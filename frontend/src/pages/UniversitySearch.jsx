import React, { useState, useEffect } from 'react';
import { universitiesAPI } from '../services/api';

export default function UniversitySearch() {
  const [universities, setUniversities] = useState([]);
  const [countries, setCountries] = useState([]);
  const [filters, setFilters] = useState({ country: '', research: '', has_scholarship: '' });
  const [loading, setLoading] = useState(false);
  const [discovering, setDiscovering] = useState(false);

  useEffect(() => {
    loadCountries();
    searchUniversities();
  }, []);

  const loadCountries = async () => {
    try {
      const response = await universitiesAPI.getCountries();
      setCountries(response.data.countries || []);
    } catch (error) {
      console.error('Error loading countries:', error);
    }
  };

  const searchUniversities = async () => {
    setLoading(true);
    try {
      const response = await universitiesAPI.search(filters);
      setUniversities(response.data.universities || []);
    } catch (error) {
      console.error('Error searching universities:', error);
    } finally {
      setLoading(false);
    }
  };

  const discoverUniversities = async () => {
    setDiscovering(true);
    try {
      await universitiesAPI.discover({ country: filters.country, limit: 50 });
      alert('Universities discovered successfully!');
      searchUniversities();
    } catch (error) {
      alert('Error discovering universities');
    } finally {
      setDiscovering(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Universities</h1>
        <button
          onClick={discoverUniversities}
          disabled={discovering}
          className="btn-primary"
        >
          {discovering ? 'Discovering...' : '🔍 Discover Universities'}
        </button>
      </div>

      {/* Filters */}
      <div className="glass-card p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <select
            value={filters.country}
            onChange={(e) => setFilters({...filters, country: e.target.value})}
            className="input-field"
          >
            <option value="">All Countries</option>
            {countries.map(country => (
              <option key={country} value={country}>{country}</option>
            ))}
          </select>
          <input
            type="text"
            placeholder="Research Area"
            value={filters.research}
            onChange={(e) => setFilters({...filters, research: e.target.value})}
            className="input-field"
          />
          <button onClick={searchUniversities} className="btn-primary">
            Search
          </button>
        </div>
      </div>

      {/* Results */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading ? (
          <div className="col-span-full text-center py-12">Loading...</div>
        ) : universities.length === 0 ? (
          <div className="col-span-full text-center py-12 text-gray-500">
            No universities found. Try discovering new ones!
          </div>
        ) : (
          universities.map(uni => (
            <div key={uni.id} className="glass-card p-6">
              <h3 className="font-semibold text-lg mb-2">{uni.name}</h3>
              <p className="text-gray-600 text-sm mb-4">📍 {uni.country}</p>
              {uni.has_scholarship && (
                <span className="px-3 py-1 bg-green-100 text-green-700 text-xs rounded-full">
                  💰 Scholarships Available
                </span>
              )}
              <div className="mt-4">
                <a href={uni.website} target="_blank" rel="noopener noreferrer" className="text-primary-600 text-sm">
                  Visit Website →
                </a>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
