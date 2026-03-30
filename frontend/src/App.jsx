import Chat from "./components/Chat.jsx";

export default function App() {
  return (
    <div className="app-root">
      <header className="app-header">
        <div className="header-chrome" aria-hidden="true" />
        <p className="header-mark" aria-hidden="true">
          ✦
        </p>
        <h1>Food Planner</h1>
        <p className="tagline">Nutrition-oriented meal planning</p>
      </header>
      <main className="app-main">
        <Chat />
      </main>
    </div>
  );
}
