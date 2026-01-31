import { JobCard } from "@/components/JobCard";
import { Job } from "@/types/job";

async function getJobs(): Promise<Job[]> {
  // Fetching data from the backend API
  // Using 'no-store' to ensure we always get fresh data (SSR behavior)
  try {
    const res = await fetch("http://127.0.0.1:8000/jobs/?limit=100", {
      cache: "no-store"
    });

    if (!res.ok) {
      throw new Error(`Failed to fetch jobs: ${res.statusText}`);
    }

    return res.json();
  } catch (error) {
    console.error("Error fetching jobs:", error);
    return [];
  }
}

export default async function Home() {
  const jobs = await getJobs();

  // Sort jobs by ID descending (newest first)
  jobs.sort((a, b) => b.id - a.id);

  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        <div className="mb-10 text-center">
          <h1 className="text-4xl font-extrabold text-gray-900 mb-2 tracking-tight">
            Jobs<span className="text-blue-600">Optimizer</span>
          </h1>
          <p className="text-lg text-gray-600">
            Encontrá tu próximo desafío en tecnología. Curado y optimizado.
          </p>
        </div>

        {jobs.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-xl shadow-sm border border-gray-100">
            <p className="text-gray-500 text-lg">
              No se encontraron ofertas por el momento. <br />
              <span className="text-sm">Asegúrate de que el backend esté corriendo.</span>
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
            {jobs.map((job) => (
              <JobCard key={job.id} job={job} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
