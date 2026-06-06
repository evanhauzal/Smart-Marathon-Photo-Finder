import {
  ScanFace,
  Hash,
  Upload,
  Search,
  Images,
  ArrowRight
} from 'lucide-react';
import { MinimalistHero } from '@/components/ui/minimalist-hero';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  const navLinks = [
    { label: 'HOME', href: '#' },
    { label: 'FACE SEARCH', href: '#features' },
    { label: 'BIB SEARCH', href: '#features' },
    { label: 'PHOTOGRAPHER', href: '/photographer' },
    { label: 'LOGIN', href: '/login' },
  ];

  const socialLinks = [];

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <MinimalistHero
        logoText="SMART MARATHON"
        navLinks={navLinks}
        mainText="Find your marathon photos instantly using face recognition and bib number search technology."
        readMoreLink="#features"
        imageSrc="/ORANG.png"
        imageAlt="Marathon runner"
        overlayText={{
          part1: 'FIND YOUR',
          part2: 'MARATHON PHOTOS',
        }}
        socialLinks={socialLinks}
        locationText="Smart Marathon Photo Finder"
      />

      {/* Features Section */}
      <section id="features" className="px-6 py-24 md:px-12 lg:px-24">
        <div className="mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="mb-16 text-center"
          >
            <h2 className="mb-4 text-4xl font-bold text-foreground md:text-5xl">
              Search <span className="text-primary">Features</span>
            </h2>
            <p className="mx-auto max-w-lg text-muted-foreground">
              Two powerful ways to find your marathon photos
            </p>
          </motion.div>

          <div className="grid gap-8 md:grid-cols-2">
            {/* Face Search Card */}
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="group relative overflow-hidden rounded-2xl border border-border bg-card p-8 transition-all duration-300 hover:border-primary/50 hover:shadow-[0_0_30px_rgba(234,179,8,0.1)]"
            >
              <div className="mb-6 flex h-14 w-14 items-center justify-center rounded-xl bg-primary/10">
                <ScanFace className="h-7 w-7 text-primary" />
              </div>
              <h3 className="mb-3 text-2xl font-bold text-foreground">Face Search</h3>
              <p className="mb-6 text-muted-foreground leading-relaxed">
                Upload a selfie and find marathon photos using ArcFace face recognition.
              </p>
              <Link
                to="/login"
                className="inline-flex items-center gap-2 text-sm font-semibold tracking-wider text-primary transition-colors hover:text-primary/80"
              >
                TRY NOW <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Link>
            </motion.div>

            {/* Bib Number Search Card */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="group relative overflow-hidden rounded-2xl border border-border bg-card p-8 transition-all duration-300 hover:border-primary/50 hover:shadow-[0_0_30px_rgba(234,179,8,0.1)]"
            >
              <div className="mb-6 flex h-14 w-14 items-center justify-center rounded-xl bg-primary/10">
                <Hash className="h-7 w-7 text-primary" />
              </div>
              <h3 className="mb-3 text-2xl font-bold text-foreground">Bib Number Search</h3>
              <p className="mb-6 text-muted-foreground leading-relaxed">
                Enter your bib number and find marathon photos instantly.
              </p>
              <Link
                to="/login"
                className="inline-flex items-center gap-2 text-sm font-semibold tracking-wider text-primary transition-colors hover:text-primary/80"
              >
                TRY NOW <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
              </Link>
            </motion.div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="px-6 py-24 md:px-12 lg:px-24">
        <div className="mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="mb-16 text-center"
          >
            <h2 className="mb-4 text-4xl font-bold text-foreground md:text-5xl">
              How It <span className="text-primary">Works</span>
            </h2>
            <p className="mx-auto max-w-lg text-muted-foreground">
              Find your photos in three simple steps
            </p>
          </motion.div>

          <div className="grid gap-8 md:grid-cols-3">
            {/* Step 1 */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="text-center"
            >
              <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full border-2 border-primary bg-primary/10">
                <Upload className="h-7 w-7 text-primary" />
              </div>
              <div className="mb-3 text-sm font-bold tracking-widest text-primary">STEP 1</div>
              <h3 className="mb-2 text-xl font-bold text-foreground">Upload Selfie or Enter Bib Number</h3>
              <p className="text-sm text-muted-foreground">
                Choose your preferred search method
              </p>
            </motion.div>

            {/* Step 2 */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.25 }}
              className="text-center"
            >
              <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full border-2 border-primary bg-primary/10">
                <Search className="h-7 w-7 text-primary" />
              </div>
              <div className="mb-3 text-sm font-bold tracking-widest text-primary">STEP 2</div>
              <h3 className="mb-2 text-xl font-bold text-foreground">System Searches Event Photos</h3>
              <p className="text-sm text-muted-foreground">
                AI-powered matching across all event photos
              </p>
            </motion.div>

            {/* Step 3 */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.4 }}
              className="text-center"
            >
              <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full border-2 border-primary bg-primary/10">
                <Images className="h-7 w-7 text-primary" />
              </div>
              <div className="mb-3 text-sm font-bold tracking-widest text-primary">STEP 3</div>
              <h3 className="mb-2 text-xl font-bold text-foreground">View Matching Results</h3>
              <p className="text-sm text-muted-foreground">
                Browse and download your marathon photos
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border px-6 py-12 md:px-12">
        <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 md:flex-row">
          <div className="text-lg font-bold tracking-wider text-foreground">
            SMART MARATHON
          </div>
          <p className="text-sm text-muted-foreground">
            Smart Marathon Photo Finder
          </p>
          <p className="text-xs text-muted-foreground/60">
            © 2026 All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
