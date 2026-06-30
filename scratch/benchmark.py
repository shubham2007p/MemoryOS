import asyncio
import time
import httpx

async def run_benchmark():
    print("--- Starting MemoryOS API Latency Benchmark ---")
    async with httpx.AsyncClient(timeout=60.0) as client:
        # 1. Profile Health endpoint
        t0 = time.perf_counter()
        res = await client.get("http://localhost:8000/api/health")
        latency_health = (time.perf_counter() - t0) * 1000
        print(f"Health API Latency: {latency_health:.2f} ms (Status: {res.status_code})")

        # 2. Profile List Sessions
        t0 = time.perf_counter()
        res = await client.get("http://localhost:8000/api/sessions")
        latency_sessions = (time.perf_counter() - t0) * 1000
        print(f"List Sessions Latency: {latency_sessions:.2f} ms (Status: {res.status_code})")

        # 3. Create a test session
        res = await client.post("http://localhost:8000/api/sessions", json={"metadata": {"test": "benchmark"}})
        session_id = res.json()["session_id"]
        print(f"Created Session ID: {session_id}")

        # 4. Profile Learner Ingestion Ingest Latency
        t0 = time.perf_counter()
        res = await client.post("http://localhost:8000/api/specialists/learner", json={
            "session_id": session_id,
            "text": "MemoryOS uses kuzu graph DB for storing Cognee entities."
        })
        latency_ingest = (time.perf_counter() - t0) * 1000
        print(f"Learner Ingestion Latency: {latency_ingest:.2f} ms (Status: {res.status_code})")

        # 5. Profile Developer Recall Reasoning Latency
        t0 = time.perf_counter()
        res = await client.post("http://localhost:8000/api/specialists/developer", json={
            "session_id": session_id,
            "query": "What database does MemoryOS use?"
        })
        latency_query = (time.perf_counter() - t0) * 1000
        print(f"Developer Recall/Reasoning Latency: {latency_query:.2f} ms (Status: {res.status_code})")

        # Clean up session
        await client.delete(f"http://localhost:8000/api/sessions/{session_id}")
        print("Benchmark session cleaned up.")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
