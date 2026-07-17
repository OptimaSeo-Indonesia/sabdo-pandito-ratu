export default function Home() {
  return (
    <main className="mx-auto max-w-4xl px-4 py-12">
      <header className="mb-12 text-center">
        <h1 className="mb-2 text-4xl font-bold">Sabdo Pandito Ratu</h1>
        <p className="text-lg text-gray-600">
          Multi-AI Deliberation Engine
        </p>
      </header>

      <section className="mb-8 rounded-lg border bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-semibold">Submit a Question</h2>
        <form
          onSubmit={async (e) => {
            e.preventDefault();
            const form = e.target as HTMLFormElement;
            const data = new FormData(form);
            const resp = await fetch("/api/v1/deliberate", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                question: data.get("question"),
              }),
            });
            const result = await resp.json();
            console.log(result);
          }}
        >
          <textarea
            name="question"
            rows={4}
            className="mb-4 w-full rounded border p-3"
            placeholder="Ask a question for the council of AI advisors..."
          />
          <button
            type="submit"
            className="rounded bg-blue-600 px-6 py-2 text-white hover:bg-blue-700"
          >
            Deliberate
          </button>
        </form>
      </section>
    </main>
  );
}
