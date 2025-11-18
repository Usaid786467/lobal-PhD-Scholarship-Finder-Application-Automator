import React, { useState, useEffect } from 'react';
import { applicationsAPI } from '../services/api';

export default function Applications() {
  const [applications, setApplications] = useState([]);
  const [filter, setFilter] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadApplications();
  }, [filter]);

  const loadApplications = async () => {
    setLoading(true);
    try {
      const response = await applicationsAPI.getAll({ status: filter });
      setApplications(response.data.applications || []);
    } catch (error) {
      console.error('Error loading applications:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (appId, newStatus) => {
    try {
      await applicationsAPI.update(appId, { status: newStatus });
      loadApplications();
    } catch (error) {
      alert('Error updating status');
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Applications</h1>

      {/* Filter */}
      <div className="glass-card p-6">
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="input-field"
        >
          <option value="">All Statuses</option>
          <option value="draft">Draft</option>
          <option value="sent">Sent</option>
          <option value="opened">Opened</option>
          <option value="replied">Replied</option>
          <option value="rejected">Rejected</option>
        </select>
      </div>

      {/* Applications List */}
      <div className="space-y-4">
        {loading ? (
          <div className="text-center py-12">Loading...</div>
        ) : applications.length === 0 ? (
          <div className="text-center py-12 text-gray-500">No applications found</div>
        ) : (
          applications.map(app => (
            <div key={app.id} className="glass-card p-6">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-lg">{app.professor_name}</h3>
                  <p className="text-gray-600 text-sm">{app.university_name}</p>
                  <p className="text-gray-500 text-sm mt-2">📧 {app.professor_email}</p>
                  {app.applied_date && (
                    <p className="text-gray-500 text-sm">
                      Applied: {new Date(app.applied_date).toLocaleDateString()}
                    </p>
                  )}
                </div>
                <div className="flex flex-col items-end gap-2">
                  <select
                    value={app.status}
                    onChange={(e) => updateStatus(app.id, e.target.value)}
                    className="input-field text-sm"
                  >
                    <option value="draft">Draft</option>
                    <option value="sent">Sent</option>
                    <option value="opened">Opened</option>
                    <option value="replied">Replied</option>
                    <option value="rejected">Rejected</option>
                  </select>
                  {app.match_score > 0 && (
                    <span className="text-sm text-gray-600">
                      Match: {app.match_score.toFixed(0)}%
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
