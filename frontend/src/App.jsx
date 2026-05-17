import { useState, useEffect } from "react";

function App() {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Baad mein real API se connect karenge
   fetch("http://localhost:8000/api/reviews")
  .then(res => res.json())
  .then(data => {
    setReviews(data);
    setLoading(false);
  })
  .catch(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white">🤖 AI Code Reviewer</h1>
        <p className="text-gray-400 mt-1">Automated PR reviews powered by Claude AI</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-gray-800 rounded-xl p-4">
          <p className="text-gray-400 text-sm">Total Reviews</p>
          <p className="text-2xl font-bold">{reviews.length}</p>
        </div>
        <div className="bg-gray-800 rounded-xl p-4">
          <p className="text-gray-400 text-sm">Completed</p>
          <p className="text-2xl font-bold text-green-400">
            {reviews.filter(r => r.status === "done").length}
          </p>
        </div>
        <div className="bg-gray-800 rounded-xl p-4">
          <p className="text-gray-400 text-sm">Total Cost</p>
          <p className="text-2xl font-bold text-yellow-400">
            ${reviews.reduce((a, r) => a + r.cost, 0).toFixed(3)}
          </p>
        </div>
      </div>

      {/* Reviews Table */}
      <div className="bg-gray-800 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-gray-700">
          <h2 className="font-semibold">Recent PR Reviews</h2>
        </div>
        {loading ? (
          <p className="p-6 text-gray-400">Loading...</p>
        ) : (
          <table className="w-full">
            <thead className="bg-gray-700 text-gray-300 text-sm">
              <tr>
                <th className="text-left p-3">Repository</th>
                <th className="text-left p-3">PR</th>
                <th className="text-left p-3">Title</th>
                <th className="text-left p-3">Status</th>
                <th className="text-left p-3">Tokens</th>
                <th className="text-left p-3">Cost</th>
              </tr>
            </thead>
            <tbody>
              {reviews.map(r => (
                <tr key={r.id} className="border-t border-gray-700 hover:bg-gray-750">
                  <td className="p-3 text-sm">{r.repo}</td>
                  <td className="p-3 text-sm">#{r.pr}</td>
                  <td className="p-3 text-sm">{r.title}</td>
                  <td className="p-3 text-sm">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      r.status === "done" 
                        ? "bg-green-900 text-green-300" 
                        : "bg-yellow-900 text-yellow-300"
                    }`}>
                      {r.status}
                    </span>
                  </td>
                  <td className="p-3 text-sm">{r.tokens}</td>
                  <td className="p-3 text-sm">${r.cost.toFixed(3)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default App;