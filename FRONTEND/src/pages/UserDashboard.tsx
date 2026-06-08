import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  ScanFace,
  Hash,
  Upload,
  LogOut,
  Home,
  Images,
} from 'lucide-react';
import API_URL from '../services/api';

const UserDashboard = () => {
  const navigate = useNavigate();

  const [activeTab, setActiveTab] = useState<'face' | 'bib'>('face');

  const [selfie, setSelfie] = useState<File | null>(null);
  const [bibNumber, setBibNumber] = useState('');

  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  const searchByFace = async () => {
    try {
      const token = localStorage.getItem('token');

      if (!token) {
        alert('Please login first');
        navigate('/login');
        return;
      }

      if (!selfie) {
        alert('Please select a selfie');
        return;
      }

      setLoading(true);

      const formData = new FormData();
      formData.append('selfie', selfie);

      const response = await fetch(
        `${API_URL}/api/search/face`,
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Face search failed');
      }

      setResults(data.matches || []);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  const searchByBib = async () => {
    try {
      const token = localStorage.getItem('token');

      if (!token) {
        alert('Please login first');
        navigate('/login');
        return;
      }

      if (!bibNumber.trim()) {
        alert('Please enter a bib number');
        return;
      }

      setLoading(true);

      const formData = new FormData();
      formData.append('bib_number', bibNumber);

      const response = await fetch(
        `${API_URL}/api/search/bib`,
        {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Bib search failed');
      }

      setResults(data.matches || []);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border px-6 py-4">
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <Link
            to="/"
            className="text-lg font-bold tracking-wider text-foreground"
          >
            SMART MARATHON
          </Link>

          <div className="flex items-center gap-4">
            <Link
              to="/"
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              <Home className="h-4 w-4" />
            </Link>

            <button
              onClick={handleLogout}
              className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              <LogOut className="h-4 w-4" />
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="mx-auto max-w-6xl px-6 py-10">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <h1 className="mb-2 text-3xl font-bold text-foreground">
            Find Your Photos
          </h1>

          <p className="mb-8 text-muted-foreground">
            Choose a search method to find your marathon photos
          </p>
        </motion.div>

        {/* Tab Selector */}
        <div className="mb-8 flex gap-3">
          <button
            onClick={() => setActiveTab('face')}
            className={`flex items-center gap-2 rounded-lg px-5 py-3 text-sm font-medium transition-all ${
              activeTab === 'face'
                ? 'bg-primary text-primary-foreground'
                : 'border border-border bg-card text-muted-foreground hover:text-foreground'
            }`}
          >
            <ScanFace className="h-4 w-4" />
            Face Search
          </button>

          <button
            onClick={() => setActiveTab('bib')}
            className={`flex items-center gap-2 rounded-lg px-5 py-3 text-sm font-medium transition-all ${
              activeTab === 'bib'
                ? 'bg-primary text-primary-foreground'
                : 'border border-border bg-card text-muted-foreground hover:text-foreground'
            }`}
          >
            <Hash className="h-4 w-4" />
            Bib Number Search
          </button>
        </div>

        {/* Face Search */}
        {activeTab === 'face' && (
          <motion.div
            key="face"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="rounded-2xl border border-border bg-card p-8"
          >
            <h2 className="mb-2 text-xl font-bold text-foreground">
              Face Search
            </h2>

            <p className="mb-6 text-sm text-muted-foreground">
              Upload a selfie and our AI will find photos of you
            </p>

            <div className="mb-6 flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-border bg-background p-12">
              <Upload className="mb-4 h-10 w-10 text-muted-foreground" />

              <input
                type="file"
                accept="image/*"
                onChange={(e) =>
                  setSelfie(e.target.files?.[0] || null)
                }
                className="mt-4"
              />

              {selfie && (
                <p className="mt-4 text-sm text-primary">
                  {selfie.name}
                </p>
              )}
            </div>

            <button
              onClick={searchByFace}
              disabled={loading}
              className="flex items-center gap-2 rounded-lg bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
            >
              <ScanFace className="h-4 w-4" />

              {loading ? 'Searching...' : 'Search Photos'}
            </button>
          </motion.div>
        )}

        {/* Bib Search */}
        {activeTab === 'bib' && (
          <motion.div
            key="bib"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="rounded-2xl border border-border bg-card p-8"
          >
            <h2 className="mb-2 text-xl font-bold text-foreground">
              Bib Number Search
            </h2>

            <p className="mb-6 text-sm text-muted-foreground">
              Enter your bib number
            </p>

            <div className="mb-6 flex gap-3">
              <input
                type="text"
                value={bibNumber}
                onChange={(e) => setBibNumber(e.target.value)}
                placeholder="Enter bib number..."
                className="flex-1 rounded-lg border border-border bg-background px-4 py-3 text-sm text-foreground"
              />

              <button
                onClick={searchByBib}
                disabled={loading}
                className="flex items-center gap-2 rounded-lg bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
              >
                <Hash className="h-4 w-4" />

                {loading ? 'Searching...' : 'Search'}
              </button>
            </div>
          </motion.div>
        )}

        {/* Results */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4 }}
          className="mt-8 rounded-2xl border border-border bg-card p-8"
        >
          <h3 className="mb-4 text-lg font-bold text-foreground">
            Search Results ({results.length})
          </h3>

          {results.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <Images className="mb-4 h-12 w-12 text-muted-foreground/30" />

              <p className="text-sm text-muted-foreground">
                No search results yet.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {results.map((item, index) => (
                <div
                  key={index}
                  className="rounded-lg border border-border p-4"
                >
                  <p>
                    <strong>Event:</strong> {item.event_dir}
                  </p>

                  <p>
                    <strong>File:</strong> {item.filename}
                  </p>

                  {item.similarity && (
                    <p>
                      <strong>Similarity:</strong>{' '}
                      {item.similarity}
                    </p>
                  )}

                  {item.detected_numbers && (
                    <p>
                      <strong>Detected Bib:</strong>{' '}
                      {item.detected_numbers.join(', ')}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default UserDashboard;