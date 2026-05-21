"use client"

import { useEffect, useState } from "react"

import api from "@/lib/api"

type Candidate = {
  id: number
  name: string
  role: string
  stage: string
  ai_score: string
  days_in_stage: number
  strengths: string
  missing_skills: string
  experience_years: number
  communication_score: string
  priority: string
  resume_summary: string
  resume_text: string
  email: string
}

export default function RecruitmentPage() {
  const [candidates, setCandidates] =
    useState<Candidate[]>([])

  const [loading, setLoading] =
    useState(true)

  const [role, setRole] =
    useState("Software Engineer")

  const [file, setFile] =
    useState<File | null>(null)

  const [uploading, setUploading] =
    useState(false)

  const [filterStage, setFilterStage] =
    useState("All")

  const [selectedCandidate, setSelectedCandidate] =
    useState<any>(null)

  const [summaryCandidate, setSummaryCandidate] =
    useState<any>(null)

  const [timeline, setTimeline] =
    useState<any[]>([])

  const [showInterviewModal, setShowInterviewModal] =
    useState(false)

  const [interviewDate, setInterviewDate] =
    useState("")

  const [interviewTime, setInterviewTime] =
    useState("")

  const [meetingLink, setMeetingLink] =
    useState("")

  const [mailPreview, setMailPreview] =
    useState("")

  // =========================
  // FETCH CANDIDATES
  // =========================

  useEffect(() => {
    fetchCandidates()
  }, [])

  const fetchCandidates = async () => {
    try {
      const response = await api.get(
        "/recruitment/candidates"
      )

      setCandidates(response.data)

      setLoading(false)
    } catch (error) {
      console.error(error)

      setLoading(false)
    }
  }

  // =========================
  // UPLOAD RESUME
  // =========================

  const uploadResume = async () => {
    if (!file) {
      alert("Select a resume")

      return
    }

    setUploading(true)

    try {
      const formData = new FormData()

      formData.append("file", file)

      formData.append("role", role)

      await api.post(
        "/recruitment/upload-resume",
        formData
      )

      fetchCandidates()

      setUploading(false)

      alert(
        "Resume analyzed successfully"
      )
    } catch (error) {
      console.error(error)

      setUploading(false)
    }
  }

  // =========================
  // CHANGE STAGE
  // =========================

  const recruiterAction = async (
    candidate: any,
    action: string
  ) => {
    try {
      await api.patch(
        `/recruitment/candidate/${candidate.id}/action?action=${action}`
      )

      if (action === "Interview") {
        setSelectedCandidate(candidate)

        setShowInterviewModal(true)

        return
      }

      fetchCandidates()
    } catch (error) {
      console.error(error)
    }
  }

  // =========================
  // DELETE CANDIDATE
  // =========================

  const deleteCandidate = async (
    id: number
  ) => {
    try {
      await api.delete(
        `/recruitment/candidate/${id}`
      )

      fetchCandidates()
    } catch (error) {
      console.error(error)
    }
  }

  // =========================
  // FETCH TIMELINE
  // =========================

  const fetchTimeline = async (
    candidateId: number
  ) => {
    try {
      const response = await api.get(
        `/recruitment/candidate/${candidateId}/timeline`
      )

      setTimeline(response.data)
    } catch (error) {
      console.error(error)
    }
  }

  // =========================
  // GENERATE MAIL
  // =========================

  const generateInterviewMail = () => {
    const mail = `
Hi ${selectedCandidate?.name},

We reviewed your profile and would like to invite you for an interview.

Interview Details:

Date: ${interviewDate}

Time: ${interviewTime}

Meeting Link:
${meetingLink}

Please confirm your availability.

Regards,
Recruitment Team
`

    setMailPreview(mail)
  }

  // =========================
  // SEND MAIL
  // =========================

  const sendInterviewMail = async () => {
    try {
      await api.post(
        "/mail/send-interview-mail",
        {
          email: selectedCandidate.email,

          candidate_name:
            selectedCandidate.name,

          date: interviewDate,

          time: interviewTime,

          meeting_link: meetingLink
        }
      )

      alert("Interview mail sent")

      setShowInterviewModal(false)

      fetchCandidates()
    } catch (error) {
      console.error(error)
    }
  }

  // =========================
  // AVG ATS
  // =========================

  const averageATS =
    candidates.length > 0
      ? Math.round(
          candidates.reduce(
            (acc, candidate) =>
              acc +
              parseInt(
                candidate.ai_score
              ),
            0
          ) / candidates.length
        )
      : 0

  return (
    <div className="space-y-6">
      {/* TITLE */}

      <div>
        <h1 className="text-3xl font-bold">
          Recruitment Intelligence
        </h1>

        <p className="mt-2 text-sm text-gray-400">
          AI-powered hiring workflow operations
        </p>
      </div>

      {/* ATS */}

      <div className="rounded-3xl border border-white/10 bg-[#111827] p-8">
        <h2 className="text-2xl font-semibold">
          AI Resume Scanner
        </h2>

        <div className="mt-6 grid gap-4 md:grid-cols-3">
          <select
            value={role}
            onChange={(e) =>
              setRole(e.target.value)
            }
            className="rounded-2xl border border-white/10 bg-[#1F2937] p-4"
          >
            <option>
              Software Engineer
            </option>

            <option>
              Operations Team
            </option>

            <option>
              Sales Team
            </option>
          </select>

          <input
            type="file"
            accept=".pdf"
            onChange={(e) => {
              if (
                e.target.files?.[0]
              ) {
                setFile(
                  e.target.files[0]
                )
              }
            }}
            className="rounded-2xl border border-white/10 bg-[#1F2937] p-4"
          />

          <button
            onClick={uploadResume}
            className="rounded-2xl bg-cyan-500 px-6 py-4 font-semibold text-black"
          >
            {uploading
              ? "Analyzing..."
              : "Analyze Resume"}
          </button>
        </div>
      </div>

      {/* FILTERS */}

      <div className="flex flex-wrap gap-3">
        {[
          "All",
          "Screening",
          "Shortlisted",
          "Interview",
          "Offer",
          "Hired",
          "Reject"
        ].map((stage) => (
          <button
            key={stage}
            onClick={() =>
              setFilterStage(stage)
            }
            className={`rounded-full px-4 py-2 text-sm ${
              filterStage === stage
                ? "bg-cyan-500 text-black"
                : "bg-[#111827] text-gray-300"
            }`}
          >
            {stage}
          </button>
        ))}
      </div>

      {/* METRICS */}

      <div className="grid gap-4 md:grid-cols-4">
        <MetricCard
          title="Candidates"
          value={candidates.length}
        />

        <MetricCard
          title="High ATS"
          value={
            candidates.filter(
              (c) =>
                parseInt(
                  c.ai_score
                ) >= 90
            ).length
          }
        />

        <MetricCard
          title="Avg ATS"
          value={`${averageATS}%`}
        />

        <MetricCard
          title="Interview Stage"
          value={
            candidates.filter(
              (c) =>
                c.stage ===
                "Interview"
            ).length
          }
        />
      </div>

      {/* CANDIDATES */}

      {loading ? (
        <div className="rounded-3xl bg-[#111827] p-10 text-center">
          Loading...
        </div>
      ) : (
        <div className="grid gap-5 lg:grid-cols-2">
          {candidates
            .filter((candidate) => {
              if (
                filterStage === "All"
              )
                return true

              return (
                candidate.stage ===
                filterStage
              )
            })
            .map((candidate) => {
              const ats = parseInt(
                candidate.ai_score
              )

              return (
                <div
                  key={candidate.id}
                  className="rounded-3xl border border-white/10 bg-[#111827] p-6"
                >
                  {/* TOP */}

                  <div className="flex items-start justify-between">
                    <div>
                      <h2 className="text-2xl font-semibold">
                        {
                          candidate.name
                        }
                      </h2>
                      <p className="mt-2 text-sm text-gray-400">
    {candidate.email}
  </p>
                      <p className="mt-2 text-gray-400">
                        {
                          candidate.role
                        }
                      </p>
                    </div>

                    <span className="rounded-full bg-red-500/20 px-4 py-2 text-xs text-red-300">
                      {
                        candidate.priority
                      }
                    </span>
                  </div>

                  {/* ATS */}

                  <div className="mt-6">
                    <div className="mb-3 flex items-center justify-between">
                      <p className="text-sm text-gray-400">
                        ATS Match
                      </p>

                      <p className="font-semibold text-cyan-300">
                        {
                          candidate.ai_score
                        }
                      </p>
                    </div>

                    <div className="h-3 overflow-hidden rounded-full bg-white/10">
                      <div
                        className={`h-full rounded-full ${
                          ats >= 90
                            ? "bg-green-400"
                            : ats >= 70
                            ? "bg-yellow-400"
                            : "bg-red-400"
                        }`}
                        style={{
                          width:
                            candidate.ai_score
                        }}
                      />
                    </div>
                  </div>

                  {/* INFO */}

                  <div className="mt-6 grid grid-cols-2 gap-4">
                    <InfoCard
                      title="Stage"
                      value={
                        candidate.stage
                      }
                    />

                    <InfoCard
                      title="Experience"
                      value={`${candidate.experience_years} yrs`}
                    />
                  </div>

                  {/* WORKFLOW */}

                  <div className="mt-6">
                    <p className="text-xs text-gray-400">
                      Workflow Stage
                    </p>

                    <select
                      value={
                        candidate.stage
                      }
                      onChange={(e) =>
                        recruiterAction(
                          candidate,
                          e.target.value
                        )
                      }
                      className="mt-3 w-full rounded-2xl border border-white/10 bg-[#1F2937] px-4 py-4"
                    >
                      <option value="Screening">
                        Screening
                      </option>

                      <option value="Shortlisted">
                        Shortlisted
                      </option>

                      <option value="Interview">
                        Interview
                      </option>

                      <option value="Offer">
                        Offer
                      </option>

                      <option value="Hired">
                        Hired
                      </option>

                      <option value="Reject">
                        Reject
                      </option>
                    </select>
                  </div>

                  {/* ACTIONS */}

                  <div className="mt-6 flex flex-wrap items-center gap-3">
                    <button
                      onClick={() => {
                        setSelectedCandidate(
                          candidate
                        )

                        fetchTimeline(
                          candidate.id
                        )
                      }}
                      className="rounded-2xl border border-white/10 px-5 py-3 text-sm transition hover:bg-white/5"
                    >
                      Timeline
                    </button>

                    <button
                      onClick={() =>
                        setSummaryCandidate(
                          candidate
                        )
                      }
                      className="rounded-2xl border border-cyan-500/20 bg-cyan-500/10 px-5 py-3 text-sm text-cyan-300 transition hover:bg-cyan-500/20"
                    >
                      AI Summary
                    </button>

                    <button
                      onClick={() =>
                        deleteCandidate(
                          candidate.id
                        )
                      }
                      className="rounded-2xl border border-red-500/20 bg-red-500/10 px-5 py-3 text-sm text-red-300 transition hover:bg-red-500/20"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              )
            })}
        </div>
      )}

      {/* SUMMARY MODAL */}

      {summaryCandidate && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
          <div className="max-h-[90vh] w-[900px] overflow-y-auto rounded-3xl bg-[#111827] p-8">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-3xl font-bold">
                  AI Resume Intelligence
                </h2>

                <p className="mt-2 text-gray-400">
                  {
                    summaryCandidate.name
                  }
                </p>
              </div>

              <button
                onClick={() =>
                  setSummaryCandidate(
                    null
                  )
                }
                className="text-3xl"
              >
                ×
              </button>
            </div>

            {/* AI SUMMARY */}

            <div className="mt-8 rounded-3xl border border-cyan-500/20 bg-cyan-500/5 p-6">
              <h3 className="text-xl font-semibold text-cyan-300">
                AI Candidate Summary
              </h3>

              <div className="mt-5 whitespace-pre-wrap leading-8 text-gray-300">
                {
                  summaryCandidate.resume_summary
                }
              </div>
            </div>

            {/* RESUME */}

            <div className="mt-8 rounded-3xl border border-white/10 bg-black/20 p-6">
              <h3 className="text-xl font-semibold">
                Resume Preview
              </h3>

              <div className="mt-5 max-h-[400px] overflow-y-auto rounded-2xl bg-[#0F172A] p-5 text-sm leading-7 text-gray-400">
                {
                  summaryCandidate.resume_text
                }
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TIMELINE MODAL */}

      {selectedCandidate &&
        !showInterviewModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
            <div className="max-h-[80vh] w-[700px] overflow-y-auto rounded-3xl bg-[#111827] p-8">
              <div className="flex items-center justify-between">
                <h2 className="text-3xl font-bold">
                  Candidate Timeline
                </h2>

                <button
                  onClick={() =>
                    setSelectedCandidate(
                      null
                    )
                  }
                  className="text-2xl"
                >
                  ×
                </button>
              </div>

              <div className="mt-8 space-y-5">
                {timeline.map((item) => (
                  <div
                    key={item.id}
                    className="rounded-2xl border border-white/10 p-5"
                  >
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold text-cyan-300">
                        {item.action}
                      </h3>

                      <p className="text-xs text-gray-500">
                        {new Date(
                          item.created_at
                        ).toLocaleString()}
                      </p>
                    </div>

                    <p className="mt-3 text-gray-300">
                      {
                        item.description
                      }
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

      {/* INTERVIEW MODAL */}

      {showInterviewModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
          <div className="w-[700px] rounded-3xl bg-[#111827] p-8">
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold">
                Schedule Interview
              </h2>

              <button
                onClick={() =>
                  setShowInterviewModal(
                    false
                  )
                }
                className="text-2xl"
              >
                ×
              </button>
            </div>

            <div className="mt-8 grid gap-4">
              <input
                type="date"
                value={interviewDate}
                onChange={(e) =>
                  setInterviewDate(
                    e.target.value
                  )
                }
                className="rounded-2xl border border-white/10 bg-[#1F2937] p-4"
              />

              <input
                type="time"
                value={interviewTime}
                onChange={(e) =>
                  setInterviewTime(
                    e.target.value
                  )
                }
                className="rounded-2xl border border-white/10 bg-[#1F2937] p-4"
              />

              <input
                type="text"
                placeholder="Meeting Link"
                value={meetingLink}
                onChange={(e) =>
                  setMeetingLink(
                    e.target.value
                  )
                }
                className="rounded-2xl border border-white/10 bg-[#1F2937] p-4"
              />

              <button
                onClick={
                  generateInterviewMail
                }
                className="rounded-2xl bg-blue-500 px-5 py-4 font-semibold"
              >
                Generate Mail
              </button>

              {mailPreview && (
                <div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-5">
                  <pre className="whitespace-pre-wrap text-sm text-gray-300">
                    {mailPreview}
                  </pre>
                </div>
              )}

              <button
                onClick={
                  sendInterviewMail
                }
                className="rounded-2xl bg-green-500 px-5 py-4 font-semibold text-black"
              >
                Send Interview Mail
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

// =========================
// METRIC CARD
// =========================

function MetricCard({
  title,
  value
}: any) {
  return (
    <div className="rounded-2xl bg-[#111827] p-5">
      <p className="text-sm text-gray-400">
        {title}
      </p>

      <h2 className="mt-3 text-3xl font-bold">
        {value}
      </h2>
    </div>
  )
}

// =========================
// INFO CARD
// =========================

function InfoCard({
  title,
  value
}: any) {
  return (
    <div className="rounded-2xl bg-black/20 p-4">
      <p className="text-xs text-gray-400">
        {title}
      </p>

      <p className="mt-2 text-lg font-semibold">
        {value}
      </p>
    </div>
  )
}