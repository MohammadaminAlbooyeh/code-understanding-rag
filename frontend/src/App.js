import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import HomePage from './pages/HomePage';
import CodeUploadPage from './pages/CodeUploadPage';
import AnalysisPage from './pages/AnalysisPage';
import DocumentationPage from './pages/DocumentationPage';
import QAPage from './pages/QAPage';
import ReviewPage from './pages/ReviewPage';
import RefactoringPage from './pages/RefactoringPage';
import DependencyPage from './pages/DependencyPage';
import HistoryPage from './pages/HistoryPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <div className="app-body">
          <Sidebar />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/upload" element={<CodeUploadPage />} />
              <Route path="/analysis/:id" element={<AnalysisPage />} />
              <Route path="/docs/:id" element={<DocumentationPage />} />
              <Route path="/qa/:id" element={<QAPage />} />
              <Route path="/review/:id" element={<ReviewPage />} />
              <Route path="/refactor/:id" element={<RefactoringPage />} />
              <Route path="/dependencies" element={<DependencyPage />} />
              <Route path="/history" element={<HistoryPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
