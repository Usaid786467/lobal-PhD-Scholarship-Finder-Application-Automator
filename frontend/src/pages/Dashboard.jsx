import React, { useState, useEffect } from 'react';
import { analyticsAPI, applicationsAPI } from '../services/api';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const response = await analyticsAPI.getDashboard();
      setStats(response.data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-12">Loading...</div>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Applications"
          value={stats?.total_applications || 0}
          icon="📝"
          color="blue"
        />
        <StatsCard
          title="Sent Applications"
          value={stats?.sent_applications || 0}
          icon="✉️"
          color="green"
        />
        <StatsCard
          title="Replies Received"
          value={stats?.replied_applications || 0}
          icon="💬"
          color="purple"
        />
        <StatsCard
          title="Response Rate"
          value={`${stats?.response_rate || 0}%`}
          icon="📊"
          color="orange"
        />
      </div>

      {/* Quick Actions */}
      <div className="glass-card p-6">
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <ActionButton
            title="Discover Universities"
            description="Find new PhD programs"
            link="/universities"
            icon="🎓"
          />
          <ActionButton
            title="Find Professors"
            description="Search for potential supervisors"
            link="/professors"
            icon="👨‍🏫"
          />
          <ActionButton
            title="Generate Emails"
            description="Create personalized emails"
            link="/emails"
            icon="✉️"
          />
        </div>
      </div>

      {/* Application Status */}
      {stats?.applications_by_status && (
        <div className="glass-card p-6">
          <h2 className="text-xl font-semibold mb-4">Application Status</h2>
          <div className="space-y-2">
            {Object.entries(stats.applications_by_status).map(([status, count]) => (
              <div key={status} className="flex justify-between items-center py-2 border-b">
                <span className="capitalize">{status}</span>
                <span className="font-semibold">{count}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function StatsCard({ title, value, icon, color }) {
  const colors = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    purple: 'from-purple-500 to-purple-600',
    orange: 'from-orange-500 to-orange-600',
  };

  return (
    <div className="glass-card p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-600 text-sm">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
        </div>
        <div className={`text-4xl bg-gradient-to-br ${colors[color]} p-3 rounded-lg`}>
          {icon}
        </div>
      </div>
    </div>
  );
}

function ActionButton({ title, description, link, icon }) {
  return (
    <a
      href={link}
      className="block p-6 bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl hover:shadow-lg transition-all duration-200"
    >
      <div className="text-4xl mb-3">{icon}</div>
      <h3 className="font-semibold text-gray-900">{title}</h3>
      <p className="text-sm text-gray-600 mt-1">{description}</p>
    </a>
  );
}
