import React, { useState, useEffect } from 'react';
import { analyticsAPI } from '../services/api';

export default function Analytics() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const [dashboard, uniStats, profStats] = await Promise.all([
        analyticsAPI.getDashboard(),
        analyticsAPI.getUniversityStats(),
        analyticsAPI.getProfessorStats()
      ]);

      setStats({
        dashboard: dashboard.data,
        universities: uniStats.data,
        professors: profStats.data
      });
    } catch (error) {
      console.error('Error loading analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-12">Loading analytics...</div>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Analytics</h1>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card p-6">
          <h3 className="text-gray-600 text-sm">Total Universities</h3>
          <p className="text-3xl font-bold mt-2">{stats?.universities?.total_universities || 0}</p>
        </div>
        <div className="glass-card p-6">
          <h3 className="text-gray-600 text-sm">Total Professors</h3>
          <p className="text-3xl font-bold mt-2">{stats?.professors?.total_professors || 0}</p>
        </div>
        <div className="glass-card p-6">
          <h3 className="text-gray-600 text-sm">Response Rate</h3>
          <p className="text-3xl font-bold mt-2">{stats?.dashboard?.response_rate || 0}%</p>
        </div>
      </div>

      {/* Universities by Country */}
      {stats?.universities?.by_country && (
        <div className="glass-card p-6">
          <h2 className="text-xl font-semibold mb-4">Universities by Country</h2>
          <div className="space-y-2">
            {Object.entries(stats.universities.by_country).map(([country, count]) => (
              <div key={country} className="flex justify-between items-center py-2 border-b">
                <span>{country}</span>
                <span className="font-semibold">{count}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Application Status Distribution */}
      {stats?.dashboard?.applications_by_status && (
        <div className="glass-card p-6">
          <h2 className="text-xl font-semibold mb-4">Application Status Distribution</h2>
          <div className="space-y-3">
            {Object.entries(stats.dashboard.applications_by_status).map(([status, count]) => {
              const total = Object.values(stats.dashboard.applications_by_status).reduce((a, b) => a + b, 0);
              const percentage = total > 0 ? (count / total * 100).toFixed(1) : 0;

              return (
                <div key={status}>
                  <div className="flex justify-between mb-1">
                    <span className="capitalize">{status}</span>
                    <span>{count} ({percentage}%)</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary-600 h-2 rounded-full"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
