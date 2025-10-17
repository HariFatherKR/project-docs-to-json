'use client'

import { useState } from 'react'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000'

export default function Home() {
  const [fileName, setFileName] = useState<string>('')
  const [jsonResult, setJsonResult] = useState<string>('')
  const [status, setStatus] = useState<'idle' | 'uploading' | 'error' | 'success'>('idle')
  const [error, setError] = useState<string>('')

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    setFileName(file.name)
    const formData = new FormData()
    formData.append('file', file, file.name)

    setStatus('uploading')
    setError('')
    setJsonResult('')

    try {
      const response = await fetch(`${API_BASE}/convert`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        const details = await response.json()
        throw new Error(details?.detail ?? 'Failed to convert document')
      }

      const data = await response.json()
      setJsonResult(JSON.stringify(data.document, null, 2))
      setStatus('success')
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Unexpected error'
      setError(message)
      setStatus('error')
    }
  }

  const downloadJson = () => {
    if (!jsonResult) return
    const blob = new Blob([jsonResult], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = `${fileName || 'document'}.json`
    anchor.click()
    URL.revokeObjectURL(url)
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col gap-6 px-6 py-16">
      <header>
        <h1 className="text-3xl font-bold">Document-to-JSON Converter</h1>
        <p className="mt-2 text-base text-slate-600">
          Upload a PDF or DOCX file to preview the structured JSON described in the MVP PRD.
        </p>
      </header>

      <section>
        <label
          htmlFor="file-input"
          className="flex w-full cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-300 bg-white py-16 text-center transition hover:border-slate-500">
          <span className="text-lg font-medium text-slate-700">Drag & drop or click to upload</span>
          <span className="mt-2 text-sm text-slate-500">Supports PDF and DOCX up to 10 MB</span>
          <input
            id="file-input"
            type="file"
            accept=".pdf,.docx"
            className="hidden"
            onChange={handleFileChange}
          />
        </label>
        {fileName && (
          <p className="mt-2 text-sm text-slate-600">Selected file: {fileName}</p>
        )}
      </section>

      <section className="rounded-xl bg-white p-6 shadow-sm">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">JSON Preview</h2>
          <button
            disabled={!jsonResult}
            onClick={downloadJson}
            className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:bg-slate-300"
          >
            Download JSON
          </button>
        </div>

        <div className="mt-4 min-h-[200px] rounded-lg bg-slate-900 p-4 text-left text-sm text-lime-200">
          {status === 'idle' && <p>Upload a document to see the parsed structure.</p>}
          {status === 'uploading' && <p>Processing… this usually takes a few seconds.</p>}
          {status === 'success' && <pre className="overflow-auto whitespace-pre-wrap">{jsonResult}</pre>}
          {status === 'error' && (
            <p className="text-red-300">Error: {error}</p>
          )}
        </div>
      </section>
    </main>
  )
}
