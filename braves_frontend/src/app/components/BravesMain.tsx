"use client";

import React, { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

interface Batter {
  BATTER_ID: number;
  BATTER: string;
}

interface Pitcher {
  PITCHER_ID: number;
  PITCHER: string;
}

interface Prediction {
  batting_average: number;
  slugging_percentage: number;
  total_at_bats: number;
  hits: number;
  strikeouts: number;
  outcome_counts: { PLAY_OUTCOME: string; count: number }[];
  performance_over_time: { date: string; batting_average: number }[];
  video_links: string[]; // Added this line
}

const API_BASE_URL = "http://localhost:8000/api";

export default function BravesMain() {
  const [batters, setBatters] = useState<Batter[]>([]);
  const [pitchers, setPitchers] = useState<Pitcher[]>([]);
  const [selectedBatter, setSelectedBatter] = useState<number | null>(null);
  const [selectedPitcher, setSelectedPitcher] = useState<number | null>(null);
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const [battersResponse, pitchersResponse] = await Promise.all([
          fetch(`${API_BASE_URL}/batters/`),
          fetch(`${API_BASE_URL}/pitchers/`),
        ]);

        if (!battersResponse.ok || !pitchersResponse.ok) {
          throw new Error("Failed to fetch player data.");
        }

        const [battersData, pitchersData] = await Promise.all([
          battersResponse.json(),
          pitchersResponse.json(),
        ]);

        setBatters(battersData);
        setPitchers(pitchersData);
      } catch (err) {
        setError("Error fetching player data. Please try again.");
        console.error(err);
      }
    };
    fetchPlayers();
  }, []);

  useEffect(() => {
    const fetchPrediction = async () => {
      if (selectedBatter && selectedPitcher) {
        try {
          const response = await fetch(
            `${API_BASE_URL}/predict/?batter_id=${selectedBatter}&pitcher_id=${selectedPitcher}`
          );

          if (!response.ok) {
            throw new Error("Failed to fetch prediction data.");
          }

          const data = await response.json();
          setPrediction(data);
        } catch (err) {
          setError("Error fetching prediction data. Please try again.");
          console.error(err);
        }
      } else {
        setPrediction(null);
      }
    };
    fetchPrediction();
  }, [selectedBatter, selectedPitcher]);

  const handleBatterChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedBatter(parseInt(event.target.value, 10));
    setPrediction(null);
  };

  const handlePitcherChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedPitcher(parseInt(event.target.value, 10));
    setPrediction(null);
  };

  const selectedBatterName = batters.find(
    (batter) => batter.BATTER_ID === selectedBatter
  )?.BATTER;
  const selectedPitcherName = pitchers.find(
    (pitcher) => pitcher.PITCHER_ID === selectedPitcher
  )?.PITCHER;

  if (error) return <p className="text-center mt-4 text-red-500">{error}</p>;

  const COLORS = [
    "#0088FE",
    "#00C49F",
    "#FFBB28",
    "#FF8042",
    "#AA336A",
    "#8884d8",
  ];

  return (
    <div className="p-4 max-w-screen-lg mx-auto">
      <section className="mt-4">
        <h2 className="text-lg font-semibold border-b-2 border-black pb-2 text-gray-800">
          Select Batter and Pitcher
        </h2>
        <div className="flex space-x-4 mt-4">
          <select
            className="p-2 border rounded"
            onChange={handleBatterChange}
            value={selectedBatter || ""}
          >
            <option value="" disabled>
              Select Batter
            </option>
            {batters.map((batter) => (
              <option key={batter.BATTER_ID} value={batter.BATTER_ID}>
                {batter.BATTER}
              </option>
            ))}
          </select>
          <select
            className="p-2 border rounded"
            onChange={handlePitcherChange}
            value={selectedPitcher || ""}
          >
            <option value="" disabled>
              Select Pitcher
            </option>
            {pitchers.map((pitcher) => (
              <option key={pitcher.PITCHER_ID} value={pitcher.PITCHER_ID}>
                {pitcher.PITCHER}
              </option>
            ))}
          </select>
        </div>
      </section>

      {prediction && prediction.video_links.length > 0 && (
        <section className="mt-6">
          <h2 className="text-lg font-semibold border-b-2 border-black pb-2 text-gray-800">
            Video Highlights
          </h2>
          <div className="mt-4 p-4 border rounded bg-gray-100">
            {prediction.video_links.map((link, index) => (
              <div key={index} className="mb-4">
                <video width="100%" controls>
                  <source src={link} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
              </div>
            ))}
          </div>
        </section>
      )}

      {prediction && (
        <>
          <section className="mt-6">
            <h2 className="text-lg font-semibold border-b-2 border-black pb-2 text-gray-800">
              {selectedBatterName} vs. {selectedPitcherName}
            </h2>
            <div className="mt-4 p-4 border rounded bg-gray-100">
              <p>
                <strong>Batting Average:</strong>{" "}
                {prediction.batting_average.toFixed(3)}
              </p>
              <p>
                <strong>Slugging Percentage:</strong>{" "}
                {prediction.slugging_percentage.toFixed(3)}
              </p>
              <p>
                <strong>Total At-Bats:</strong> {prediction.total_at_bats}
              </p>
              <p>
                <strong>Hits:</strong> {prediction.hits}
              </p>
              <p>
                <strong>Strikeouts:</strong> {prediction.strikeouts}
              </p>
            </div>
          </section>

          <section className="mt-6">
            <h2 className="text-lg font-semibold border-b-2 border-black pb-2 text-gray-800">
              Outcome Distribution
            </h2>
            <div className="mt-4 p-4 border rounded bg-gray-100">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={prediction.outcome_counts}>
                  <XAxis dataKey="PLAY_OUTCOME" />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </section>

          {prediction.performance_over_time && (
            <section className="mt-6">
              <h2 className="text-lg font-semibold border-b-2 border-black pb-2 text-gray-800">
                Batting Average Over Time
              </h2>
              <div className="mt-4 p-4 border rounded bg-gray-100">
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={prediction.performance_over_time}>
                    <XAxis dataKey="date" />
                    <YAxis domain={[0, 1]} />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="batting_average"
                      stroke="#82ca9d"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </section>
          )}

          <section className="mt-6">
            <h2 className="text-lg font-semibold border-b-2 border-black pb-2 text-gray-800">
              Outcome Percentage
            </h2>
            <div className="mt-4 p-4 border rounded bg-gray-100">
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={prediction.outcome_counts}
                    dataKey="count"
                    nameKey="PLAY_OUTCOME"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label
                  >
                    {prediction.outcome_counts.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </section>
        </>
      )}
    </div>
  );
}
