import Chat from "./components/Chat.jsx";
import { SectionHeart } from "./components/SectionHeart.jsx";
import { SoftSmokeBackground } from "./components/ui/SoftSmokeBackground.jsx";

export default function App() {
  return (
    <SoftSmokeBackground>
      <div className="landing-page">
        <header className="landing-hero">
          <p className="landing-eyebrow">Gentle nutrition · plain language</p>
          <h1>An everyday companion for meals—not rigid rules.</h1>
          <p className="landing-lead">
            Meal ideas, balanced swaps, and approachable guidance. Ask in your own
            words; answers stay grounded and calm.
          </p>
        </header>

        <SectionHeart />

        <section className="landing-features" aria-label="How it helps">
          <article className="feature-card">
            <h2>Meals that fit you</h2>
            <p>
              Suggestions you can tweak—vegetarian, higher protein, quick
              weeknights, or whatever you need today.
            </p>
          </article>
          <article className="feature-card">
            <h2>Why, not just what</h2>
            <p>
              Short explanations when you want them, so choices feel clearer
              without a lecture.
            </p>
          </article>
        </section>

        <SectionHeart />

        <p className="landing-trust">
          This chat offers general food and diet information only. It is not
          medical advice and does not replace a clinician or registered
          dietitian for your personal health needs.
        </p>

        <SectionHeart />

        <div className="landing-chat-intro">
          <h2>Try the chat</h2>
          <p>Pick a prompt or write your own—conversation stays in this tab.</p>
        </div>

        <Chat />
      </div>
    </SoftSmokeBackground>
  );
}
