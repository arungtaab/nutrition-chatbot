import Chat from "./components/Chat.jsx";
import { SectionDecoDivider } from "./components/SectionDecoDivider.jsx";
import { DecoShell } from "./components/ui/DecoShell.jsx";

export default function App() {
  return (
    <DecoShell>
      <div className="deco-landing">
        <header className="deco-hero deco-hero--editorial">
          <div className="deco-hero-frame">
            <p className="deco-eyebrow deco-reveal deco-reveal--1">
              Nutrition salon · your table, your rules
            </p>
            <h1 className="deco-hero-title deco-reveal deco-reveal--2">
              Nourish
            </h1>
            <p className="deco-hero-tagline deco-reveal deco-reveal--3">
              Meal ideas for whoever’s cooking—not a one-size diet script.
            </p>
            <p className="deco-lead deco-reveal deco-reveal--4">
              Say what you avoid (allergies, faith-based choices, plant-based,
              whatever) and what you’re in the mood for. Replies stay plain-spoken
              and grounded in the docs this instance knows.
            </p>
          </div>
          <p
            className="deco-stack deco-reveal deco-reveal--5"
            aria-label="Tech stack"
          >
            <span className="deco-stack-inner">
              React · Vite · Flask · RAG · SQLite
            </span>
          </p>
        </header>

        <SectionDecoDivider />

        <section className="deco-features" aria-label="How it helps">
          <article className="deco-feature">
            <h2>Meals that fit you</h2>
            <p>
              Omnivore, plant-forward, halal, kosher-style, low-sodium, picky
              kids—name your lane. I built it around my own skips (no meat,
              poultry, fish, or eggs) but the chat works for anyone who types
              their boundaries in plain English.
            </p>
          </article>
        </section>

        <SectionDecoDivider />

        <aside className="deco-trust deco-reveal deco-reveal--6">
          <p className="deco-trust-label">Notice</p>
          <p className="deco-trust-body">
            This chat offers general food and diet information only. It is not
            medical advice and does not replace a clinician or registered
            dietitian. It is also not for extreme restriction, purging, or other
            harmful eating-disorder behaviors—the app may refuse those topics.
            If food or body image feels overwhelming, consider reaching out to
            a qualified professional; in the U.S., NEDA (nationaleatingdisorders.org)
            and 988 offer support.
          </p>
        </aside>

        <SectionDecoDivider />

        <div className="deco-chat-intro deco-reveal deco-reveal--7">
          <h2 className="deco-chat-intro-title">The salon floor</h2>
          <p className="deco-chat-intro-lead">
            Try a starter below or write your own—this is your conversation on
            this page.
          </p>
        </div>

        <div className="deco-chat-row">
          <div className="deco-chat-flank deco-chat-flank--left" aria-hidden="true">
            <img
              src="/illustrations/chat-flank-left.png"
              alt=""
              width={320}
              height={640}
              decoding="async"
            />
          </div>
          <div className="deco-chat-stage">
            <Chat />
          </div>
          <div className="deco-chat-flank deco-chat-flank--right" aria-hidden="true">
            <img
              src="/illustrations/chat-flank-right.png"
              alt=""
              width={320}
              height={640}
              decoding="async"
            />
          </div>
        </div>

        <p className="deco-attribution">
          Fashion illustrations —{" "}
          <a
            href="https://www.freepik.com"
            target="_blank"
            rel="noopener noreferrer"
          >
            Designed by Freepik
          </a>
          . Vintage feminine fashion vector (George Barbier–style remix); comply
          with Freepik license terms for your distribution.
        </p>
      </div>
    </DecoShell>
  );
}
