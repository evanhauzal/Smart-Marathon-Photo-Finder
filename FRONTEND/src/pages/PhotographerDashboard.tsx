import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Upload, LogOut, Home, Images, FolderOpen } from 'lucide-react';

const PhotographerDashboard = () => {
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
          <h1 className="mb-2 text-3xl font-bold text-foreground">Photographer Portal</h1>
          <p className="mb-8 text-muted-foreground">Upload and manage marathon event photos</p>
        </motion.div>

        {/* Upload Section */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
          className="mb-8 rounded-2xl border border-border bg-card p-8"
        >
          <h2 className="mb-2 text-xl font-bold text-foreground">Upload Event Photos</h2>
          <p className="mb-6 text-sm text-muted-foreground">
            Upload marathon event photos for participants to search
          </p>

          <div className="mb-6">
            <label htmlFor="event-name" className="mb-2 block text-sm font-medium text-foreground">
              Event Name
            </label>
            <input
              id="event-name"
              type="text"
              placeholder="e.g., Jakarta Marathon 2026"
              className="w-full max-w-md rounded-lg border border-border bg-background px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
            />
          </div>

          <div className="mb-6 flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-border bg-background p-12 transition-colors hover:border-primary/50">
            <Upload className="mb-4 h-10 w-10 text-muted-foreground" />
            <p className="mb-2 text-sm font-medium text-foreground">
              Drop event photos here or click to browse
            </p>
            <p className="text-xs text-muted-foreground">
              JPG, PNG, WebP — Multiple files allowed
            </p>
            <input
              type="file"
              accept="image/*"
              multiple
              className="mt-4 text-sm text-muted-foreground file:mr-4 file:rounded-lg file:border-0 file:bg-primary file:px-4 file:py-2 file:text-sm file:font-semibold file:text-primary-foreground hover:file:bg-primary/90"
            />
          </div>

          <button className="flex items-center gap-2 rounded-lg bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground transition-colors hover:bg-primary/90">
            <Upload className="h-4 w-4" />
            Upload Photos
          </button>
        </motion.div>

        {/* Uploaded Photos Gallery */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.2 }}
          className="rounded-2xl border border-border bg-card p-8"
        >
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-xl font-bold text-foreground">Uploaded Photos</h2>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <FolderOpen className="h-4 w-4" />
              <span>0 events</span>
            </div>
          </div>

          <div className="flex flex-col items-center justify-center py-12 text-center">
            <Images className="mb-4 h-12 w-12 text-muted-foreground/30" />
            <p className="text-sm text-muted-foreground">
              No photos uploaded yet. Upload event photos to get started.
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default PhotographerDashboard;
