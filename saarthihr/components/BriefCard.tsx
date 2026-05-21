export default function BriefCard() {
  return (
    <div className="rounded-3xl bg-gradient-to-r from-teal-500/20 to-cyan-500/10 p-8">
      <h1 className="text-4xl font-bold">
        Good Morning 👋
      </h1>

      <div className="mt-5 space-y-2 text-gray-300">
        <p>• Backend hiring delayed by 3 days</p>

        <p>• 2 candidates pending feedback</p>

        <p>• GitHub access pending for onboarding</p>
      </div>
    </div>
  )
}