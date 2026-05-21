type Props = {
  title: string
  value: string
}

export default function MetricCard({
  title,
  value,
}: Props) {
  return (
    <div className="rounded-2xl border border-white/10 bg-[#111827] p-6">
      <p className="text-sm text-gray-400">
        {title}
      </p>

      <h2 className="mt-4 text-4xl font-bold">
        {value}
      </h2>
    </div>
  )
}