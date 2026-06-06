import { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ScanFace, Hash, Upload, LogOut, Home, Images } from 'lucide-react';

const UserDashboard = () => {
  const [activeTab, setActiveTab] = useState<'face' | 'bib'>('face');

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border px-6 py-4">
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <Link to="/" className="text-lg font-bold tracking-wider text-foreground">
            SMART MARATHON
          </Link>
          <div className="flex items-center gap-4">
            <Link to="/" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              <Home className="h-4 w-4" />
            </Link>
            <Link
              to="/login"
              className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              <LogOut className="h-4 w-4" />
              Logout
            </Link>
          </div>
        </div>
      </nav>

      <div className="mx-auto max-w-6xl px-6 py-10">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <h1 className="mb-2 text-3xl font-bold text-foreground">Find Your Photos</h1>
          <p className="mb-8 text-muted-foreground">Choose a search method to find your marathon photos</p>
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

        {/* Face Search Panel */}
        {activeTab === 'face' && (
          <motion.div
            key="face"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="rounded-2xl border border-border bg-card p-8"
          >
            <h2 className="mb-2 text-xl font-bold text-foreground">Face Search</h2>
            <p className="mb-6 text-sm text-muted-foreground">
              Upload a selfie and our AI will find photos of you from marathon events
            </p>

            <div className="mb-6 flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-border bg-background p-12 transition-colors hover:border-primary/50">
              <Upload className="mb-4 h-10 w-10 text-muted-foreground" />
              <p className="mb-2 text-sm font-medium text-foreground">
                Drop your selfie here or click to browse
              </p>
              <p className="text-xs text-muted-foreground">
                JPG, PNG, WebP — Max 10MB
              </p>
              <input
                type="file"
                accept="image/*"
                className="mt-4 text-sm text-muted-foreground file:mr-4 file:rounded-lg file:border-0 file:bg-primary file:px-4 file:py-2 file:text-sm file:font-semibold file:text-primary-foreground hover:file:bg-primary/90"
              />
            </div>

            <button className="flex items-center gap-2 rounded-lg bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground transition-colors hover:bg-primary/90">
              <ScanFace className="h-4 w-4" />
              Search Photos
            </button>
          </motion.div>
        )}

        {/* Bib Number Search Panel */}
        {activeTab === 'bib' && (
          <motion.div
            key="bib"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="rounded-2xl border border-border bg-card p-8"
          >
            <h2 className="mb-2 text-xl font-bold text-foreground">Bib Number Search</h2>
            <p className="mb-6 text-sm text-muted-foreground">
              Enter your bib number to find photos from marathon events
            </p>

            <div className="mb-6 flex gap-3">
              <input
                type="text"
                placeholder="Enter your bib number..."
                className="flex-1 rounded-lg border border-border bg-background px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
              />
              <button className="flex items-center gap-2 rounded-lg bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground transition-colors hover:bg-primary/90">
                <Hash className="h-4 w-4" />
                Search
              </button>
            </div>
          </motion.div>
        )}

        {/* Results Area */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="mt-8 rounded-2xl border border-border bg-card p-8"
        >
          <h3 className="mb-4 text-lg font-bold text-foreground">Search Results</h3>
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <Images className="mb-4 h-12 w-12 text-muted-foreground/30" />
            <p className="text-sm text-muted-foreground">
              No search results yet. Upload a selfie or enter a bib number to search.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default UserDashboard;
