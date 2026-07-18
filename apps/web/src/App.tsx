import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/layout";
import Home from "./pages/Home";
import Session from "./pages/Session";
import Sessions from "./pages/Sessions";
import Placeholder from "./pages/Placeholder";

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/session/:id" element={<Session />} />
          <Route path="/sessions" element={<Sessions />} />
          <Route path="/deliberations" element={<Sessions />} />
          <Route path="/council" element={<Placeholder title="Council" subtitle="Manage AI advisor personas and configurations" />} />
          <Route path="/knowledge" element={<Placeholder title="Knowledge Base" subtitle="Upload documents, set preferences, and manage context sources" />} />
          <Route path="/analytics" element={<Placeholder title="Analytics" subtitle="Track deliberation metrics, wisdom scores, and usage patterns" />} />
          <Route path="/settings" element={<Placeholder title="Settings" subtitle="Configure API providers, models, and system preferences" />} />
          <Route path="/docs" element={<Placeholder title="Documentation" subtitle="API reference, integration guides, and system architecture" />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
