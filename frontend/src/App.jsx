import { useState, useEffect } from "react"


export default function App() {
  const [reviews, setReviews] = useState([])
  const [stats, setStats] = useState({ total: 0, repos: 0 })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulated data for now — will connect to real API later
    setTimeout(() => {
      setReviews([
        {
          id: 1,
          pr_number: 1,
          repo: "AREEBA-ZIA/ai-code-reviewer",
          title: "Test webhook",
          status: "reviewed",
          time: "2 hours ago",
          summary: "AI review completed successfully."
        }
      ])
      setStats({ total: 1, repos: 1 })
      setLoading(false)
    }, 1000)
  }, [])

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Header */}
      <header className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-sm font-bold">AI</div>
          <h1 className="text-lg font-semibold">AI Code Reviewer</h1>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-purple-600 flex items-center justify-center text-sm font-bold">A</div>
          <span className="text-sm text-gray-400">AREEBA-ZIA</span>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <p className="text-gray-400 text-sm mb-1">Total Reviews</p>
            <p className="text-3xl font-bold text-blue-400">{stats.total}</p>
          </div>
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <p className="text-gray-400 text-sm mb-1">Repositories</p>
            <p className="text-3xl font-bold text-purple-400">{stats.repos}</p>
          </div>
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <p className="text-gray-400 text-sm mb-1">Status</p>
            <p className="text-3xl font-bold text-green-400">Active</p>
          </div>
        </div>

        {/* Reviews List */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl">
          <div className="px-6 py-4 border-b border-gray-800">
            <h2 className="font-semibold">Recent PR Reviews</h2>
          </div>

          {loading ? (
            <div className="px-6 py-12 text-center text-gray-500">Loading reviews...</div>
          ) : reviews.length === 0 ? (
            <div className="px-6 py-12 text-center text-gray-500">No reviews yet. Open a PR to get started!</div>
          ) : (
            <div className="divide-y divide-gray-800">
              {reviews.map((review) => (
                <div key={review.id} className="px-6 py-4 flex items-center justify-between hover:bg-gray-800 transition">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-blue-400 text-sm font-mono">#{review.pr_number}</span>
                      <span className="font-medium">{review.title}</span>
                    </div>
                    <div className="flex items-center gap-3 text-sm text-gray-400">
                      <span>{review.repo}</span>
                      <span>•</span>
                      <span>{review.time}</span>
                    </div>
                  </div>
                  <span className="bg-green-900 text-green-400 text-xs px-3 py-1 rounded-full">
                    ✓ Reviewed
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}