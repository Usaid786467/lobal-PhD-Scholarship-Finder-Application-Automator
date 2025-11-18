import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { emailsAPI, professorsAPI } from '../services/api';

export default function EmailManagement() {
  const [searchParams] = useSearchParams();
  const [batches, setBatches] = useState([]);
  const [selectedBatch, setSelectedBatch] = useState(null);
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const profIds = searchParams.get('professors');
    if (profIds) {
      generateEmails(profIds.split(',').map(Number));
    } else {
      loadBatches();
    }
  }, [searchParams]);

  const generateEmails = async (professorIds) => {
    setLoading(true);
    try {
      await emailsAPI.generate({ professor_ids: professorIds });
      alert('Emails generated successfully!');
      loadBatches();
    } catch (error) {
      alert('Error generating emails');
    } finally {
      setLoading(false);
    }
  };

  const loadBatches = async () => {
    try {
      const response = await emailsAPI.getBatches();
      setBatches(response.data.batches || []);
    } catch (error) {
      console.error('Error loading batches:', error);
    }
  };

  const loadBatchEmails = async (batchId) => {
    try {
      const response = await emailsAPI.getBatch(batchId);
      setSelectedBatch(response.data.batch);
      setEmails(response.data.emails || []);
    } catch (error) {
      console.error('Error loading batch emails:', error);
    }
  };

  const approveBatch = async (batchId) => {
    try {
      await emailsAPI.approveBatch(batchId);
      alert('Batch approved!');
      loadBatches();
    } catch (error) {
      alert('Error approving batch');
    }
  };

  const sendBatch = async (batchId) => {
    if (!confirm('Send all emails in this batch?')) return;

    try {
      await emailsAPI.sendBatch(batchId);
      alert('Batch sent successfully!');
      loadBatches();
    } catch (error) {
      alert('Error sending batch');
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Email Management</h1>

      {loading && <div className="text-center py-12">Generating emails...</div>}

      {/* Batches List */}
      <div className="glass-card p-6">
        <h2 className="text-xl font-semibold mb-4">Email Batches</h2>
        <div className="space-y-3">
          {batches.map(batch => (
            <div key={batch.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <p className="font-medium">Batch #{batch.id}</p>
                <p className="text-sm text-gray-600">
                  {batch.sent_count}/{batch.total_count} sent • Status: {batch.status}
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => loadBatchEmails(batch.id)}
                  className="btn-secondary text-sm"
                >
                  View
                </button>
                {batch.status === 'draft' && (
                  <button
                    onClick={() => approveBatch(batch.id)}
                    className="btn-primary text-sm"
                  >
                    Approve
                  </button>
                )}
                {batch.status === 'approved' && (
                  <button
                    onClick={() => sendBatch(batch.id)}
                    className="btn-primary text-sm"
                  >
                    Send All
                  </button>
                )}
              </div>
            </div>
          ))}
          {batches.length === 0 && (
            <p className="text-gray-500 text-center py-8">No email batches yet</p>
          )}
        </div>
      </div>

      {/* Email Preview */}
      {selectedBatch && emails.length > 0 && (
        <div className="glass-card p-6">
          <h2 className="text-xl font-semibold mb-4">Batch #{selectedBatch.id} Emails</h2>
          <div className="space-y-4">
            {emails.slice(0, 5).map(email => (
              <div key={email.id} className="border rounded-lg p-4">
                <p className="font-semibold">{email.subject}</p>
                <p className="text-sm text-gray-600 mt-2 whitespace-pre-wrap">
                  {email.body.substring(0, 200)}...
                </p>
                <span className={`text-xs px-2 py-1 rounded mt-2 inline-block ${
                  email.status === 'sent' ? 'bg-green-100 text-green-700' :
                  email.status === 'approved' ? 'bg-blue-100 text-blue-700' :
                  'bg-gray-100 text-gray-700'
                }`}>
                  {email.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
