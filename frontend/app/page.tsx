"use client";

import { FormEvent, useState } from "react";

type ShortenResponse = {
  short_code: string;
  short_url: string;
  original_url: string;
};

const API_URL =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ||
  "http://localhost:8000";

export default function Home() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<ShortenResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setCopied(false);
    setResult(null);

    const value = url.trim();
    if (!value) {
      setError("Enter a URL first.");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/shorten`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: value }),
      });

      if (!response.ok) {
        const details = await response.json().catch(() => null);
        throw new Error(
          details?.detail
            ? typeof details.detail === "string"
              ? details.detail
              : "Please enter a valid URL."
            : "Unable to shorten this URL."
        );
      }

      const data: ShortenResponse = await response.json();
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unexpected error while contacting the API."
      );
    } finally {
      setLoading(false);
    }
  }

  async function copyShortUrl() {
    if (!result) return;
    try {
      await navigator.clipboard.writeText(result.short_url);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setError("Could not copy automatically. Please copy the URL manually.");
    }
  }

  return (
    <main className="shell">
      <section className="card">
        <div className="eyebrow">GENAI FOUNDATIONS · LAB 01</div>
        <h1>Shorten a long URL.</h1>
        <p className="subtitle">
          A FastAPI + Next.js URL shortener built with an AI-first workflow.
        </p>

        <form onSubmit={submit} className="form">
          <label htmlFor="url">Long URL</label>
          <div className="row">
            <input
              id="url"
              type="url"
              value={url}
              onChange={(event) => setUrl(event.target.value)}
              placeholder="https://example.com/very/long/url"
              disabled={loading}
              required
            />
            <button type="submit" disabled={loading}>
              {loading ? "Shortening…" : "Shorten"}
            </button>
          </div>
        </form>

        {error && (
          <div className="message error" role="alert">
            {error}
          </div>
        )}

        {result && (
          <div className="result" aria-live="polite">
            <span className="resultLabel">Your shortened URL</span>
            <div className="resultRow">
              <a href={result.short_url} target="_blank" rel="noreferrer">
                {result.short_url}
              </a>
              <button className="secondary" type="button" onClick={copyShortUrl}>
                {copied ? "Copied!" : "Copy"}
              </button>
            </div>
          </div>
        )}
      </section>
    </main>
  );
}
