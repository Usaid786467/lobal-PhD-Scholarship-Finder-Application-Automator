import React, { useState, useEffect } from 'react';
import { professorsAPI, universitiesAPI } from '../services/api';

export default function ProfessorSearch() {
  const [professors, setProfessors] = useState([]);
  const [universities, setUniversities] = useState([]);
  const [selectedProfessors, setSelectedProfessors] = useState([]);
  const [filters, setFilters] = useState({ university_id: '', department: '', accepting: 'true' });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadUniversities();
    searchProfessors();
  }, []);

  const loadUniversities = async () => {
    try {
      const response = await universitiesAPI.search({});
      setUniversities(response.data.universities || []);
    } catch (error) {
      console.error('Error loading universities:', error);
    }
  };

  const searchProfessors = async () => {
    setLoading(true);
    try {
      const response = await professorsAPI.search(filters);
      setProfessors(response.data.professors || []);
    } catch (error) {
      console.error('Error searching professors:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleSelection = (profId) => {
    setSelectedProfessors(prev =>
      prev.includes(profId) ? prev.filter(id => id !== profId) : [...prev, profId]
    );
  };

  const generateEmailsForSelected = () => {
    if (selectedProfessors.length === 0) {
      alert('Please select professors first');
      return;
    }
    window.location.href = `/emails?professors=${selectedProfessors.join(',')}`;
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Professors</h1>
        {selectedProfessors.length > 0 && (
          <button onClick={generateEmailsForSelected} className="btn-primary">
            ✉️ Generate {selectedProfessors.length} Emails
          </button>
        )}
      </div>

      {/* Filters */}
      <div className="glass-card p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <select
            value={filters.university_id}
            onChange={(e) => setFilters({...filters, university_id: e.target.value})}
            className="input-field"
          >
            <option value="">All Universities</option>
            {universities.map(uni => (
              <option key={uni.id} value={uni.id}>{uni.name}</option>
            ))}
          </select>
          <input
            type="text"
            placeholder="Department"
            value={filters.department}
            onChange={(e) => setFilters({...filters, department: e.target.value})}
            className="input-field"
          />
          <button onClick={searchProfessors} className="btn-primary">
            Search
          </button>
        </div>
      </div>

      {/* Results */}
      <div className="space-y-4">
        {loading ? (
          <div className="text-center py-12">Loading...</div>
        ) : professors.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            No professors found
          </div>
        ) : (
          professors.map(prof => (
            <div key={prof.id} className="glass-card p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3">
                    <input
                      type="checkbox"
                      checked={selectedProfessors.includes(prof.id)}
                      onChange={() => toggleSelection(prof.id)}
                      className="w-5 h-5"
                    />
                    <div>
                      <h3 className="font-semibold text-lg">{prof.name}</h3>
                      <p className="text-gray-600 text-sm">{prof.university_name} • {prof.department}</p>
                    </div>
                  </div>
                  {prof.email && (
                    <p className="text-sm text-gray-600 mt-2">✉️ {prof.email}</p>
                  )}
                  {prof.match_score && (
                    <div className="mt-3">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        prof.match_score >= 70 ? 'bg-green-100 text-green-700' :
                        prof.match_score >= 50 ? 'bg-yellow-100 text-yellow-700' :
                        'bg-gray-100 text-gray-700'
                      }`}>
                        Match: {prof.match_score.toFixed(0)}%
                      </span>
                    </div>
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
