type Props = {
  title: string
  severity: string
}

export default function AlertCard({
  title,
  severity,
}: Props) {
  return (
    <div className="rounded-2xl border border-red-500/20 bg-red-500/10 p-5">
      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold text-red-400">
          {severity}
        </span>

        <span className="text-sm text-gray-300">
          Active
        </span>
      </div>

      <p className="mt-3">{title}</p>
    </div>
  )
}