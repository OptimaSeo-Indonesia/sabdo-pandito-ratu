import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Session from "./pages/Session";
import Sessions from "./pages/Sessions";

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/session/:id" element={<Session />} />
          <Route path="/sessions" element={<Sessions />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
