
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
import tempfile
import os
import shutil
import time
from fastapi.responses import RedirectResponse
from app.vectordb.resume_store import clear_resume_collection
from app.pipeline.index_resumes import index_resumes
from app.pipeline.match_resumes import search_and_rank
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from app.evaluation.similarity_analysis import analyze_similarity_distribution
from app.evaluation.ranking_metrics import evaluate_single_jd


app = FastAPI(title="Resume Screening System")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

RESUME_DIR = "storage/resumes"
os.makedirs(RESUME_DIR, exist_ok=True)


def get_saved_resumes():
    return sorted(
        [
            f for f in os.listdir(RESUME_DIR)
            if os.path.isfile(os.path.join(RESUME_DIR, f))
        ]
    )


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request
    })


def get_resume_count():
    return sum(
        1 for f in os.listdir(RESUME_DIR)
        if os.path.isfile(os.path.join(RESUME_DIR, f))
    )


@app.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {
        "request": request,
        "message": None,
        "resume_count": get_resume_count()
    })


@app.post("/upload-resumes", response_class=HTMLResponse)
async def upload_resumes(request: Request, files: List[UploadFile] = File(...)):
    try:
        uploaded_count = 0
        uploaded_paths = []

        for file in files:
            if not file.filename:
                continue

            safe_name = os.path.basename(file.filename)

            # skip temp Word files
            if safe_name.startswith("~$"):
                continue

            file_path = os.path.join(RESUME_DIR, safe_name)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            uploaded_paths.append(file_path)
            uploaded_count += 1

        start = time.time()
        index_resumes(uploaded_paths)
        end = time.time()

        print(f"Indexing time: {end - start:.3f} seconds")

        resumes = get_saved_resumes()
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "message": f"{uploaded_count} resumes indexed successfully",
            "resume_count": len(resumes)
        })

    except Exception as e:
        resumes = get_saved_resumes()
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "message": f"Error: {str(e)}",
            "resume_count": len(resumes)
        })


@app.get("/match-page", response_class=HTMLResponse)
def match_page(request: Request):
    return templates.TemplateResponse("match.html", {
        "request": request,
        "results": None,
        "message": None,
        "jd_text": "",
        "top_k": 5
    })


@app.post("/match", response_class=HTMLResponse)
async def match_resumes(request: Request, jd_text: str = Form(...), top_k: int = Form(...)):
    try:
        resumes = get_saved_resumes()

        if len(resumes) == 0:
            return templates.TemplateResponse("match.html", {
                "request": request,
                "results": None,
                "message": "No resumes indexed. Please upload resumes first.",
                "jd_text": jd_text,
                "top_k": top_k
            })

        start = time.time()
        results = search_and_rank(jd_text, top_k=top_k)
        end = time.time()
        total_time = end - start
        num_resumes = len(results)
        time_per_resume = total_time / num_resumes if num_resumes > 0 else 0

        print(f"Matching time: {end - start:.3f} seconds")

        def get_relevance(result):
            label = result.get("decision", "")
            if label == "Highly Suitable":
                return 2
            elif label == "Moderately Suitable":
                return 1
            return 0

        ranked_results = [
            {
                "name": r["candidate_name"],
                "score": r["final_score"],
                "true_relevance": get_relevance(r)
            }
            for r in results
        ]

        evaluation = evaluate_single_jd(ranked_results)
        similarity_analysis = analyze_similarity_distribution(results)

        os.makedirs("evaluation_outputs", exist_ok=True)
        file_path = os.path.join("evaluation_outputs", "ranking_metrics.txt")

        with open(file_path, "w") as f:
            f.write("Ranking Evaluation Metrics\n")
            f.write("==========================\n")
            f.write(f"MRR: {evaluation['MRR']:.4f}\n")
            f.write(f"NDCG: {evaluation['NDCG']:.4f}\n")
            f.write(f"NDCG@5: {evaluation['NDCG@5']:.4f}\n")
            f.write(f"NDCG@10: {evaluation['NDCG@10']:.4f}\n")

            f.write("\nCosine Similarity Distribution Analysis\n")
            f.write("======================================\n")
            f.write(f"Matched Scores: {similarity_analysis['matched_scores']}\n")
            f.write(f"Unmatched Scores: {similarity_analysis['unmatched_scores']}\n")
            f.write(f"Average Matched Similarity: {similarity_analysis['matched_avg']:.4f}\n")
            f.write(f"Average Unmatched Similarity: {similarity_analysis['unmatched_avg']:.4f}\n")

            f.write("\nProcessing Time Analysis\n")
            f.write("========================\n")
            f.write(f"Total Matching Time: {total_time:.4f} seconds\n")
            f.write(f"Number of Resumes: {num_resumes}\n")
            f.write(f"Time per Resume: {time_per_resume:.4f} seconds\n")

        return templates.TemplateResponse("match.html", {
            "request": request,
            "results": results,
            "message": f"Matching completed in {end - start:.3f} sec.",
            "jd_text": jd_text,
            "top_k": top_k
        })

    except Exception as e:
        print("MATCH ERROR:", str(e))
        return templates.TemplateResponse("match.html", {
            "request": request,
            "results": None,
            "message": f"Error: {str(e)}",
            "jd_text": jd_text,
            "top_k": top_k
        })
@app.post("/clear-resumes")
def clear_resumes():
    if os.path.exists(RESUME_DIR):
        shutil.rmtree(RESUME_DIR)
        os.makedirs(RESUME_DIR, exist_ok=True)

    clear_resume_collection()

    return RedirectResponse(url="/upload", status_code=303)


@app.get("/download-resume/{file_name}")
def download_resume(file_name: str):
    file_path = os.path.join(RESUME_DIR, os.path.basename(file_name))

    if not os.path.exists(file_path):
        return HTMLResponse("File not found", status_code=404)

    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_name),
        media_type="application/octet-stream"
    )