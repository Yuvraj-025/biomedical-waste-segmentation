import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion, AnimatePresence } from 'framer-motion'
import { Upload, X, Image as ImageIcon, Scan, Trash2, CheckCircle, AlertTriangle, ArrowRight, Activity } from 'lucide-react'

function App() {
    const [files, setFiles] = useState([])
    const [isAnalyzing, setIsAnalyzing] = useState(false)
    const [analysisResult, setAnalysisResult] = useState(null)

    const onDrop = useCallback(acceptedFiles => {
        setFiles(acceptedFiles.map(file => Object.assign(file, {
            preview: URL.createObjectURL(file)
        })))
        setAnalysisResult(null)
    }, [])

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'image/*': []
        },
        maxFiles: 1
    })

    const removeFile = () => {
        if (files.length > 0) {
            URL.revokeObjectURL(files[0].preview)
        }
        setFiles([])
        setAnalysisResult(null)
    }

    const handleAnalyze = async () => {
        if (files.length === 0) return

        setIsAnalyzing(true)
        setAnalysisResult(null)

        const formData = new FormData()
        formData.append('file', files[0])

        try {
            const response = await fetch(`http://${window.location.hostname}:5000/predict`, {
                method: 'POST',
                body: formData,
            })

            if (!response.ok) {
                throw new Error('Analysis failed')
            }

            const data = await response.json()
            await new Promise(resolve => setTimeout(resolve, 800))
            setAnalysisResult(data)
        } catch (error) {
            console.error('Error analyzing image:', error)
            alert('Failed to analyze image. Please check backend connection.')
        } finally {
            setIsAnalyzing(false)
        }
    }

    return (
        <div className="min-h-screen w-full text-white font-sans selection:bg-cyan-500/30">

            {/* Navbar */}
            <nav className="fixed top-0 w-full z-50 border-b border-white/10 bg-slate-900/60 backdrop-blur-xl">
                <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-gradient-to-tr from-cyan-500 to-blue-600 rounded-lg shadow-lg shadow-cyan-500/20">
                            <Activity className="w-5 h-5 text-white" />
                        </div>
                        <span className="text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
                            BioWaste<span className="font-light">AI</span>
                        </span>
                    </div>
                    <div className="flex items-center gap-4">
                        <div className="hidden md:flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs text-slate-400">
                            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                            System Operational
                        </div>
                    </div>
                </div>
            </nav>

            {/* Main Content - Centered Layout */}
            <main className="pt-24 md:pt-40 pb-10 px-4 md:px-6 w-full flex flex-col items-center overflow-x-hidden">

                {/* Centered Heading Section */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="text-center mb-12 md:mb-20 space-y-4 md:space-y-6 max-w-4xl"
                >
                    <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-sm font-semibold tracking-wide backdrop-blur-sm">
                        <Scan className="w-4 h-4" /> AI-Powered Recognition
                    </div>
                    <h1 className="text-6xl md:text-8xl font-black tracking-tight leading-tight text-white mb-4">
                        Intelligent Waste <br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600">Classification</span>
                    </h1>
                    <p className="text-xl text-slate-300 max-w-2xl mx-auto leading-relaxed font-light">
                        Upload biomedical waste imagery for instant, precision-grade classification and disposal compliance recommendations.
                    </p>
                </motion.div>

                {/* Layout: Side-by-Side Cards (Balanced) */}
                <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-10 items-stretch justify-items-center mb-10">

                    {/* Upload Section */}
                    <motion.div
                        initial={{ opacity: 0, x: -30 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.3, duration: 0.7 }}
                        className="relative group w-full h-full"
                    >
                        <div className="absolute -inset-0.5 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-3xl blur opacity-15 group-hover:opacity-30 transition duration-700"></div>
                        <div className="relative h-full bg-slate-900/40 backdrop-blur-2xl border border-white/10 rounded-3xl p-8 shadow-2xl flex flex-col">
                            <div className="flex items-center justify-between mb-8">
                                <h3 className="text-2xl font-bold text-white flex items-center gap-3">
                                    <Upload className="w-6 h-6 text-cyan-400" /> Input Imagery
                                </h3>
                                {files.length > 0 && (
                                    <button
                                        onClick={removeFile}
                                        className="text-xs font-bold uppercase tracking-widest text-red-400 hover:text-red-300 transition-colors px-3 py-1 rounded-full bg-red-500/10 border border-red-500/20"
                                    >
                                        Clear
                                    </button>
                                )}
                            </div>

                            <div className="flex-grow space-y-8">
                                {files.length === 0 ? (
                                    <div
                                        {...getRootProps()}
                                        className={`border-2 border-dashed rounded-2xl h-56 md:h-80 flex flex-col items-center justify-center cursor-pointer transition-all duration-500 ${isDragActive
                                            ? 'border-cyan-500 bg-cyan-500/10'
                                            : 'border-slate-700 bg-slate-800/30 hover:border-cyan-500/40 hover:bg-slate-800/50'
                                            }`}
                                    >
                                        <input {...getInputProps()} />
                                        <div className="p-5 rounded-full bg-slate-800/50 mb-4 border border-white/5">
                                            <ImageIcon className="w-10 h-10 text-slate-400" />
                                        </div>
                                        <p className="text-white text-lg font-medium text-center">Drag & drop or click to upload</p>
                                        <p className="text-sm text-slate-500 mt-2 text-center">Biomedical Imagery (Shielded Formats)</p>
                                    </div>
                                ) : (
                                    <div className="relative rounded-2xl overflow-hidden border border-white/10 bg-black/40 h-56 md:h-80 flex items-center justify-center shadow-inner">
                                        <img
                                            src={files[0].preview}
                                            alt="Preview"
                                            className="max-w-full max-h-full object-contain p-4"
                                        />
                                        <div className="absolute top-4 right-4 p-2 bg-emerald-500/20 border border-emerald-500/30 rounded-full backdrop-blur-md">
                                            <CheckCircle className="w-4 h-4 text-emerald-400" />
                                        </div>
                                    </div>
                                )}

                                <button
                                    onClick={handleAnalyze}
                                    disabled={files.length === 0 || isAnalyzing}
                                    className={`w-full py-5 rounded-2xl font-black text-xl tracking-wide transition-all duration-500 flex items-center justify-center gap-3 ${files.length === 0
                                        ? 'bg-slate-800/50 text-slate-600 cursor-not-allowed border border-white/5'
                                        : 'bg-gradient-to-r from-cyan-600 to-blue-600 hover:scale-[1.02] active:scale-[0.98] text-white shadow-2xl shadow-cyan-500/30 border border-cyan-400/30'
                                        }`}
                                >
                                    {isAnalyzing ? (
                                        <Activity className="w-6 h-6 animate-spin text-white" />
                                    ) : (
                                        <Scan className="w-6 h-6" />
                                    )}
                                    <span className="uppercase">{isAnalyzing ? 'Processing...' : 'Run Analysis'}</span>
                                </button>
                            </div>
                        </div>
                    </motion.div>

                    {/* Results Section */}
                    <div className="w-full h-full min-h-[400px]">
                        <AnimatePresence mode="wait">
                            {analysisResult ? (
                                <motion.div
                                    key="result"
                                    initial={{ opacity: 0, x: 30 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    exit={{ opacity: 0, scale: 0.95 }}
                                    transition={{ duration: 0.6, ease: "easeOut" }}
                                    className="relative h-full"
                                >
                                    <div className="absolute -inset-0.5 bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-3xl blur opacity-20"></div>
                                    <div className="relative h-full bg-slate-900/40 backdrop-blur-2xl border border-white/10 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
                                        <div className="p-5 md:p-8 border-b border-white/5 bg-emerald-500/5 flex items-center justify-between">
                                            <div className="flex items-center gap-3">
                                                <div className="p-2 bg-emerald-500/20 rounded-lg">
                                                    <CheckCircle className="w-6 h-6 text-emerald-400" />
                                                </div>
                                                <h3 className="text-xl md:text-2xl font-bold text-white">Detailed Analytics</h3>
                                            </div>
                                            <div className="text-[10px] font-black tracking-[0.2em] text-emerald-500/60 uppercase">
                                                Verified Result
                                            </div>
                                        </div>

                                        <div className="p-5 md:p-10 space-y-6 md:space-y-12 flex-grow">
                                            <div className="space-y-2">
                                                <p className="text-xs font-black text-slate-500 uppercase tracking-[0.3em]">Classification Target</p>
                                                <h4 className="text-3xl md:text-5xl font-black text-white capitalize leading-tight">{analysisResult.class}</h4>
                                            </div>

                                            <div className="space-y-4">
                                                <div className="flex justify-between items-end">
                                                    <p className="text-xs font-black text-slate-500 uppercase tracking-[0.3em]">Match Confidence</p>
                                                    <span className="text-2xl md:text-3xl font-black text-cyan-400">{(analysisResult.confidence * 100).toFixed(1)}%</span>
                                                </div>
                                                <div className="h-4 w-full bg-white/5 rounded-full overflow-hidden border border-white/5">
                                                    <motion.div
                                                        initial={{ width: 0 }}
                                                        animate={{ width: `${analysisResult.confidence * 100}%` }}
                                                        transition={{ duration: 1.5, ease: "easeOut" }}
                                                        className="h-full bg-gradient-to-r from-cyan-600 via-blue-500 to-emerald-500"
                                                    />
                                                </div>

                                                {/* Secondary Detections for Transparency */}
                                                {analysisResult.all_detections && analysisResult.all_detections.length > 1 && (
                                                    <div className="pt-4 border-t border-white/5">
                                                        <p className="text-[10px] font-black text-slate-600 uppercase tracking-[0.2em] mb-3">Other Detections found in Frame</p>
                                                        <div className="flex flex-wrap gap-2">
                                                            {analysisResult.all_detections
                                                                .filter(d => d.name.toLowerCase() !== analysisResult.class.toLowerCase().replace(" ", "-")) // Basic filter
                                                                .slice(0, 2)
                                                                .map((det, i) => (
                                                                    <div key={i} className="px-3 py-1 rounded-full bg-white/5 border border-white/10 text-[10px] text-slate-400 font-bold uppercase">
                                                                        {det.name.trim().replace("-", " ")}: {(det.confidence * 100).toFixed(0)}%
                                                                    </div>
                                                                ))
                                                            }
                                                        </div>
                                                    </div>
                                                )}
                                            </div>

                                            <div className="p-4 md:p-6 rounded-2xl bg-gradient-to-br from-amber-500/10 via-amber-500/5 to-transparent border border-amber-500/20 shadow-xl shadow-amber-900/10">
                                                <p className="text-xs font-black text-amber-500 uppercase tracking-[0.3em] mb-4 flex items-center gap-3">
                                                    <AlertTriangle className="w-5 h-5" /> Disposal Protocol
                                                </p>
                                                <p className="text-lg md:text-2xl font-semibold text-amber-100 leading-relaxed font-sans">{analysisResult.disposal}</p>
                                            </div>
                                        </div>

                                        <div className="px-5 py-3 md:px-8 md:py-5 bg-white/[0.02] border-t border-white/5 flex justify-between items-center text-[10px] text-slate-500 font-bold uppercase tracking-[0.2em]">
                                            <div className="flex items-center gap-2">
                                                <div className="w-1.5 h-1.5 rounded-full bg-cyan-500/50"></div>
                                                ID: {Math.random().toString(36).substr(2, 9).toUpperCase()}
                                            </div>
                                            <span>Neural Core Engine v1.02</span>
                                        </div>
                                    </div>
                                </motion.div>
                            ) : (
                                <motion.div
                                    key="placeholder"
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    className="h-full flex flex-col items-center justify-center p-12 border-2 border-dashed border-white/10 rounded-3xl bg-white/[0.02] backdrop-blur-sm shadow-inner"
                                >
                                    <div className="w-24 h-24 rounded-full bg-slate-800/20 flex items-center justify-center mb-8 border border-white/5 animate-pulse">
                                        <Activity className="w-12 h-12 text-slate-700" />
                                    </div>
                                    <p className="text-slate-400 text-center font-medium text-xl leading-relaxed">
                                        Awaiting analysis data... <br />
                                        <span className="text-sm opacity-40 font-normal block mt-2">Classification metrics will appear here once processed.</span>
                                    </p>
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>

                </div>
            </main>
        </div>
    )
}

export default App
