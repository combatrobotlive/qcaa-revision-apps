from __future__ import annotations

from datetime import datetime, timezone
import base64
import html
import io
import json
import urllib.error
import urllib.request

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Combat Robot Live", page_icon="🤖", layout="wide")
st.markdown(
    """
    <style>
    .block-container {max-width:1280px;padding-top:.7rem;padding-bottom:3rem;}
    #MainMenu, footer {visibility:hidden;}
    .event-head {border:1px solid rgba(90,100,120,.2);border-radius:16px;padding:1rem 1.1rem;margin:.2rem 0 .8rem;background:rgba(120,130,145,.055);}
    .event-club {font-size:.78rem;text-transform:uppercase;letter-spacing:.1em;font-weight:850;opacity:.65;}
    .event-name {font-size:2rem;line-height:1.05;font-weight:900;margin:.18rem 0 .38rem;}
    .event-meta {font-size:.92rem;opacity:.72;}
    .health {border-radius:999px;padding:.4rem .75rem;font-weight:800;font-size:.83rem;display:inline-block;margin:.1rem 0 .7rem;}
    .health.live {background:#e9f8ef;color:#146b35;border:1px solid #72bf8b;}
    .health.warn {background:#fff5dc;color:#815900;border:1px solid #e1b951;}
    .health.bad {background:#ffeded;color:#9a1e1e;border:1px solid #dc7979;}
    .queue-card {border:3px solid #687184;border-radius:15px;padding:.85rem 1rem;margin:.45rem 0;background:rgba(120,130,145,.06);box-shadow:0 1px 4px rgba(0,0,0,.07);}
    .queue-card.red {border-color:#c62828;background:#fff0f0;color:#251717!important}.queue-card.blue {border-color:#1565c0;background:#eef6ff;color:#13263b!important}
    .queue-card.red .queue-match,.queue-card.red .queue-meta{color:#251717!important}.queue-card.blue .queue-match,.queue-card.blue .queue-meta{color:#13263b!important}
    .queue-card.now {border-width:4px;padding:1rem 1.15rem;}
    .queue-role {font-size:.78rem;font-weight:950;letter-spacing:.09em;}
    .queue-card.red .queue-role{color:#a11919}.queue-card.blue .queue-role{color:#0d55a4}
    .queue-match {font-size:1.55rem;font-weight:900;line-height:1.15;margin:.28rem 0;}
    .queue-card.now .queue-match {font-size:1.9rem;}
    .queue-meta {font-size:.86rem;opacity:.75;}
    .section-title {font-size:1.25rem;font-weight:900;margin:1.2rem 0 .45rem;}
    .upcoming {display:grid;grid-template-columns:1fr;gap:.4rem;margin:.25rem 0 .8rem;}
    .upcoming-row {display:grid;grid-template-columns:58px 72px minmax(0,1fr) auto;align-items:center;gap:.55rem;border:1px solid rgba(90,100,120,.24);border-left:5px solid #687184;border-radius:9px;padding:.48rem .6rem;background:rgba(120,130,145,.035);}
    .upcoming-row.red{border-left-color:#c62828}.upcoming-row.blue{border-left-color:#1565c0}
    .fight-no{font-weight:900}.fight-time{font-size:.8rem;opacity:.7}.fight-match{font-weight:800;min-width:0}.fight-detail{font-size:.75rem;opacity:.7;font-weight:500}
    .status-chip{font-size:.7rem;font-weight:850;padding:.2rem .42rem;border-radius:999px;background:rgba(110,120,135,.14);white-space:nowrap}
    .division-banner {border-radius:12px;padding:.62rem .78rem;margin:.65rem 0 .45rem;border:2px solid #687184;background:rgba(120,130,145,.05);}
    .division-banner.red{border-color:#c62828;background:#fff4f4;color:#251717!important}.division-banner.blue{border-color:#1565c0;background:#f2f8ff;color:#13263b!important}
    .division-banner.red .division-title,.division-banner.red .division-sub{color:#251717!important}.division-banner.blue .division-title,.division-banner.blue .division-sub{color:#13263b!important}
    .division-title{font-weight:900;font-size:1.02rem}.division-sub{font-size:.78rem;opacity:.7;text-transform:uppercase;letter-spacing:.05em;font-weight:800}
    .group-card {border:3px solid rgba(80,90,110,.55);border-radius:12px;overflow:hidden;margin:.5rem 0 1.1rem;background:rgba(120,130,145,.055);box-shadow:0 1px 4px rgba(0,0,0,.06)}
    .group-title {font-size:1.08rem;font-weight:900;padding:.55rem .75rem;background:rgba(105,115,130,.18);border-bottom:2px solid rgba(80,90,110,.4)}
    .group-card table {width:100%;border-collapse:collapse;font-size:.9rem}.group-card th{padding:.42rem .5rem;text-align:left;background:rgba(100,110,130,.10);border-bottom:2px solid rgba(80,90,110,.3)}
    .group-card td{padding:.4rem .5rem;border-bottom:1px solid rgba(90,100,120,.20)}.group-card tr.qualifier{background:rgba(55,150,90,.13)}
    a.robot-link{color:inherit!important;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:2px;font-weight:inherit}
    .profile-nav{margin:.2rem 0 .9rem}.profile-nav a{font-weight:800;text-decoration:none}
    .profile-card{border:2px solid rgba(90,100,120,.35);border-radius:16px;padding:1rem;margin:.45rem 0 1rem;background:rgba(120,130,145,.05)}
    .profile-name{font-size:2rem;font-weight:950;line-height:1.05}.profile-meta{margin-top:.3rem;opacity:.76}
    .profile-links{display:flex;flex-wrap:wrap;gap:.42rem;margin:.4rem 0 1rem}.profile-chip{border:1px solid rgba(90,100,120,.3);border-radius:999px;padding:.34rem .62rem;background:rgba(120,130,145,.06);text-decoration:none!important;font-weight:750}
    .profile-photo{border-radius:14px;overflow:hidden;border:1px solid rgba(90,100,120,.25)}
    @media (min-width: 850px){.queue-pair{display:grid;grid-template-columns:1fr 1fr;gap:.7rem}.prepare-grid{display:grid;grid-template-columns:1fr 1fr;gap:.7rem}}
    @media (max-width: 700px){
      .block-container{padding-left:.55rem;padding-right:.55rem}.event-head{padding:.8rem .85rem}.event-name{font-size:1.62rem}
      .queue-card{padding:.7rem .78rem}.queue-card.now{padding:.82rem .88rem}.queue-match{font-size:1.28rem}.queue-card.now .queue-match{font-size:1.52rem}
      .upcoming-row{grid-template-columns:48px minmax(0,1fr) auto;gap:.4rem}.fight-time{display:none}.fight-detail{font-size:.7rem}.status-chip{font-size:.64rem}
      .group-card table{font-size:.75rem}.group-card th,.group-card td{padding:.34rem .35rem}.group-card th:nth-child(3),.group-card td:nth-child(3){display:none}
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def _config():
    try:
        return str(st.secrets["SUPABASE_URL"]).rstrip("/"), str(st.secrets["SUPABASE_PUBLISHABLE_KEY"])
    except Exception:
        st.error("This public viewer has not been configured yet. The organiser needs to add the Supabase URL and publishable key to Streamlit Cloud secrets.")
        st.stop()


def fetch_current():
    base, key = _config()
    endpoint = base + "/rest/v1/live_public_events?select=event_key,event_name,snapshot,updated_at&is_active=eq.true&order=updated_at.desc&limit=1"
    req = urllib.request.Request(endpoint, headers={"apikey": key, "Accept": "application/json", "User-Agent":"CombatRobotPublicViewer/1.16"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            rows = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        st.error(f"The live-data service returned HTTP {exc.code}. {detail[:300]}")
        return None
    except Exception as exc:
        st.error(f"Could not reach the live-data service: {exc}")
        return None
    return rows[0] if rows else None


def fetch_profile(robot_id: int):
    base, key = _config()
    endpoint = base + f"/rest/v1/live_public_robot_profiles?select=profile,updated_at&robot_id=eq.{int(robot_id)}&limit=1"
    req = urllib.request.Request(endpoint, headers={"apikey": key, "Accept": "application/json", "User-Agent":"CombatRobotPublicViewer/1.16"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            rows = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        if exc.code in (404, 406):
            return None
        st.error(f"Could not load this robot profile (HTTP {exc.code}). {detail[:250]}")
        return None
    except Exception as exc:
        st.error(f"Could not load this robot profile: {exc}")
        return None
    return rows[0] if rows else None


def robot_link(name, robot_id) -> str:
    label = html.escape(str(name or "Unknown"))
    try:
        rid = int(robot_id)
    except Exception:
        return label
    return f'<a class="robot-link" href="?robot={rid}" target="_self">{label}</a>'


def profile_links_html(snapshot: dict) -> str:
    profiles = snapshot.get("robot_profiles", []) or []
    if not profiles:
        return ""
    links = []
    for robot in sorted(profiles, key=lambda r: (str(r.get("weight_class", "")), str(r.get("name", "")).casefold())):
        try:
            rid = int(robot.get("robot_id"))
        except Exception:
            continue
        name = html.escape(str(robot.get("name") or "Unknown"))
        weight = html.escape(str(robot.get("weight_class") or ""))
        suffix = f" · {weight}" if weight else ""
        links.append(f'<a class="profile-chip" href="?robot={rid}" target="_self">🤖 {name}{suffix}</a>')
    return '<div class="profile-links">' + "".join(links) + '</div>'


def category_parts(value: str):
    destructive = str(value).casefold() == "destructive"
    return ("red", "🔴", "DESTRUCTIVE") if destructive else ("blue", "🔵", "NON-DESTRUCTIVE")


def queue_card(row: dict, heading: str, *, now: bool = False) -> str:
    cls, icon, cat = category_parts(str(row.get("Type", "")))
    bits = [f"Fight {row.get('Order')}" if row.get("Order") else "", row.get("Division", ""), row.get("Stage", "")]
    if row.get("Estimated"):
        bits.append("~" + str(row["Estimated"]))
    if row.get("Arena"):
        bits.append(str(row["Arena"]))
    meta = " · ".join(str(x) for x in bits if x)
    extra = " now" if now else ""
    return f"""
    <div class="queue-card {cls}{extra}">
      <div class="queue-role">{html.escape(heading)} &nbsp; {icon} {cat}</div>
      <div class="queue-match">{robot_link(row.get('Robot_1',''), row.get('Robot_1_ID'))} <span style="opacity:.48">vs</span> {robot_link(row.get('Robot_2',''), row.get('Robot_2_ID'))}</div>
      <div class="queue-meta">{html.escape(meta)}</div>
    </div>"""


def upcoming_html(rows: list[dict], limit: int = 8) -> str:
    rendered = []
    for row in rows[:limit]:
        cls, icon, _ = category_parts(str(row.get("Type", "")))
        detail = " · ".join(str(x) for x in [row.get("Division", ""), row.get("Stage", "")] if x)
        if row.get("Group") not in (None, "", "nan"):
            detail += (" · " if detail else "") + f"Group {row.get('Group')}"
        status = str(row.get("Queue_Status") or "Waiting")
        estimated = ("~" + str(row.get("Estimated"))) if row.get("Estimated") else ""
        rendered.append(f"""
        <div class="upcoming-row {cls}">
          <div class="fight-no">#{html.escape(str(row.get('Order','')))}</div>
          <div class="fight-time">{html.escape(estimated)}</div>
          <div class="fight-match">{icon} {robot_link(row.get('Robot_1',''), row.get('Robot_1_ID'))} <span style="opacity:.45">vs</span> {robot_link(row.get('Robot_2',''), row.get('Robot_2_ID'))}<div class="fight-detail">{html.escape(detail)}</div></div>
          <div class="status-chip">{html.escape(status)}</div>
        </div>""")
    return '<div class="upcoming">' + "".join(rendered) + "</div>"


def group_letter(n: int) -> str:
    n = max(1, int(n)); out = ""
    while n:
        n, r = divmod(n - 1, 26); out = chr(65 + r) + out
    return out


def group_card(rows: list[dict], group_number: int) -> str:
    if not rows:
        return ""
    preferred = ["Position","Robot","Team","Played","Wins","Draws","Losses","Points","Against","Difference","Qualifies"]
    columns = [c for c in preferred if any(c in r for r in rows)]
    short = {"Position":"Pos","Played":"P","Wins":"W","Draws":"D","Losses":"L","Points":"Pts","Difference":"Diff","Qualifies":"Q"}
    head = "".join(f"<th>{html.escape(short.get(c,c))}</th>" for c in columns)
    body = []
    for row in rows:
        qualifier = str(row.get("Qualifies", "")).casefold() == "yes"
        cell_parts = []
        for c in columns:
            if c == "Robot":
                value = robot_link(row.get("Robot"), row.get("Robot_ID"))
            else:
                value = html.escape('' if row.get(c) is None else str(row.get(c)))
            cell_parts.append(f"<td>{value}</td>")
        cells = "".join(cell_parts)
        body.append(f"<tr class={'qualifier' if qualifier else ''}>{cells}</tr>")
    return f'<div class="group-card"><div class="group-title">Group {group_letter(group_number)}</div><div style="overflow-x:auto"><table><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div></div>'


def age_info(updated_at: str):
    try:
        dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        seconds = max(0, (datetime.now(timezone.utc) - dt.astimezone(timezone.utc)).total_seconds())
        if seconds < 60:
            human = f"{int(seconds)}s ago"
        elif seconds < 3600:
            human = f"{int(seconds // 60)}m ago"
        else:
            human = f"{int(seconds // 3600)}h ago"
        return dt, seconds, human
    except Exception:
        return None, None, "unknown"


def render_standings(snapshot: dict):
    st.markdown('<div class="section-title">Current standings</div>', unsafe_allow_html=True)
    divisions = snapshot.get("divisions", []) or []
    if not divisions:
        st.caption("Standings will appear once fights are available.")
        return
    for div in divisions:
        cls, icon, cat = category_parts(div.get("competition_type", ""))
        title = f"{icon} {div.get('weight_class','')} — {div.get('division_name','')}"
        st.markdown(
            f'<div class="division-banner {cls}"><div class="division-title">{html.escape(title)}</div><div class="division-sub">{cat}</div></div>',
            unsafe_allow_html=True,
        )
        standings = div.get("standings", []) or []
        if div.get("has_groups"):
            groups = {}
            for row in standings:
                try:
                    g = int(row.get("Group"))
                except Exception:
                    continue
                groups.setdefault(g, []).append(row)
            group_ids = sorted(groups)
            for i in range(0, len(group_ids), 2):
                batch = group_ids[i:i+2]
                cols = st.columns(len(batch))
                for col, g in zip(cols, batch):
                    with col:
                        st.markdown(group_card(groups[g], g), unsafe_allow_html=True)
        elif standings:
            st.dataframe(pd.DataFrame(standings), hide_index=True, use_container_width=True)
        finals = div.get("finals", []) or []
        if finals:
            with st.expander(f"{title} — finals bracket", expanded=True):
                st.dataframe(pd.DataFrame(finals), hide_index=True, use_container_width=True)


def render_profile(robot_id: int, current_snapshot: dict | None = None):
    row = fetch_profile(robot_id)
    st.markdown('<div class="profile-nav"><a href="?" target="_self">← Back to live competition</a></div>', unsafe_allow_html=True)
    if not row:
        st.warning("This robot profile is not available yet. The organiser may need to run the Version 1.16 Supabase profile upgrade and publish the event again.")
        return
    profile = row.get("profile") or {}
    name = str(profile.get("name") or "Robot")
    weight = str(profile.get("weight_class") or "")
    teams = ", ".join(profile.get("teams") or []) or "Team not recorded"
    st.markdown(
        f'<div class="profile-card"><div class="profile-name">🤖 {html.escape(name)}</div><div class="profile-meta">{html.escape(weight)} · {html.escape(teams)}</div></div>',
        unsafe_allow_html=True,
    )

    photos = profile.get("photos") or []
    if photos:
        cols = st.columns(min(3, len(photos)))
        for idx, photo in enumerate(photos[:3]):
            try:
                image_bytes = base64.b64decode(str(photo.get("data_base64") or ""))
            except Exception:
                continue
            with cols[idx % len(cols)]:
                caption = str(photo.get("caption") or name)
                st.image(io.BytesIO(image_bytes), caption=caption, use_container_width=True)

    rec = profile.get("record") or {}
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Fights", rec.get("fights", 0))
    m2.metric("Wins", rec.get("wins", 0))
    m3.metric("Losses", rec.get("losses", 0))
    m4.metric("Events", rec.get("events", 0))

    podium = profile.get("podium_counts") or {}
    st.markdown('<div class="section-title">Competition achievements</div>', unsafe_allow_html=True)
    p1, p2, p3 = st.columns(3)
    p1.metric("🥇 Wins", podium.get("first", 0))
    p2.metric("🥈 Seconds", podium.get("second", 0))
    p3.metric("🥉 Thirds", podium.get("third", 0))

    ratings = profile.get("ratings") or []
    if ratings:
        st.markdown('<div class="section-title">Current Elo ratings</div>', unsafe_allow_html=True)
        rating_df = pd.DataFrame(ratings).rename(columns={
            "pool":"Ranking pool", "fights":"Fights", "wins":"Wins", "draws":"Draws",
            "losses":"Losses", "rating":"Rating", "competition_type":"Type"
        })
        cols = [c for c in ["Ranking pool","Fights","Wins","Draws","Losses","Rating"] if c in rating_df.columns]
        st.dataframe(rating_df[cols], hide_index=True, use_container_width=True)

    placements = profile.get("placements") or []
    if placements:
        st.markdown('<div class="section-title">Podium history</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(placements), hide_index=True, use_container_width=True)

    recent = profile.get("recent_fights") or []
    if recent:
        st.markdown('<div class="section-title">Recent fights</div>', unsafe_allow_html=True)
        recent_df = pd.DataFrame(recent).rename(columns={
            "date":"Date", "event":"Event", "division":"Division", "type":"Type",
            "stage":"Stage", "opponent":"Opponent", "outcome":"Result", "score":"Score"
        })
        st.dataframe(recent_df, hide_index=True, use_container_width=True)

    aliases = profile.get("aliases") or []
    if aliases:
        st.caption("Also known as: " + ", ".join(str(x) for x in aliases))
    st.caption("Public robot profile · Photos are resized public copies; the organiser retains the originals locally.")


def render_snapshot(snapshot: dict, updated_at: str):
    event = snapshot.get("event", {})
    metrics = snapshot.get("metrics", {})
    dt, age, human_age = age_info(updated_at)
    health_cls = "live" if age is not None and age <= 75 else ("warn" if age is not None and age <= 150 else "bad")
    health_text = "● LIVE" if health_cls == "live" else ("● DELAYED" if health_cls == "warn" else "● POSSIBLY OFFLINE")

    club = str(event.get("club_name") or "Combat Robot Live")
    detail = " · ".join(x for x in [event.get("event_date") or "", event.get("location") or ""] if x)
    st.markdown(
        f'<div class="event-head"><div class="event-club">{html.escape(club)}</div><div class="event-name">{html.escape(str(event.get("event_name", "Combat Robot Live")))}</div><div class="event-meta">{html.escape(detail or "Live competition board")}</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="health {health_cls}">{health_text} · updated {html.escape(human_age)}</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Completed", metrics.get("completed", 0))
    c2.metric("Remaining", metrics.get("remaining", 0))
    c3.metric("Pace", f"{float(metrics.get('pace_minutes', 0)):.1f} min/fight" if metrics.get("pace_minutes") else "—")

    queue = snapshot.get("queue", {})
    if queue.get("now"):
        st.markdown(queue_card(queue["now"][0], "NOW FIGHTING", now=True), unsafe_allow_html=True)
    pair = []
    if queue.get("next"):
        pair.append(queue_card(queue["next"][0], "ON DECK / NEXT"))
    if queue.get("prepare"):
        pair.append(queue_card(queue["prepare"][0], "PREPARE"))
    if pair:
        st.markdown('<div class="queue-pair">' + "".join(pair[:2]) + '</div>', unsafe_allow_html=True)
    if queue.get("prepare") and len(queue["prepare"]) > 1:
        st.markdown(queue_card(queue["prepare"][1], "PREPARE"), unsafe_allow_html=True)
    if not any(queue.get(key) for key in ("now", "next", "prepare")):
        st.success("All scheduled fights are complete.")

    schedule = pd.DataFrame(snapshot.get("schedule", []))
    if not schedule.empty:
        pending = schedule[schedule.get("Fight_Status", pd.Series(index=schedule.index, dtype=str)).fillna("") != "Completed"].copy()
        if not pending.empty:
            st.markdown('<div class="section-title">Upcoming fights</div>', unsafe_allow_html=True)
            pending = pending.sort_values("Order", kind="stable") if "Order" in pending.columns else pending
            st.markdown(upcoming_html(pending.to_dict(orient="records"), limit=8), unsafe_allow_html=True)

    render_standings(snapshot)

    profile_links = profile_links_html(snapshot)
    if profile_links:
        st.markdown('<div class="section-title">Robot profiles</div>', unsafe_allow_html=True)
        st.markdown(profile_links, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Fight schedule and results</div>', unsafe_allow_html=True)
    if schedule.empty:
        st.info("No fights have been published yet.")
    else:
        if "Type" in schedule.columns:
            schedule["Category"] = schedule["Type"].map(lambda v: f"{category_parts(v)[1]} {v}")
        if "Queue_Status" in schedule.columns:
            schedule["Status"] = schedule["Queue_Status"]
        show_cols = [c for c in ["Order","Estimated","Division","Category","Stage","Group","Robot_1","Robot_2","Result","Status","Arena"] if c in schedule.columns]
        with st.expander("Open full schedule / completed results", expanded=False):
            st.dataframe(schedule[show_cols], hide_index=True, use_container_width=True, height=650)

    if age is not None and age > 120:
        st.warning(f"Live data has not updated for about {int(age // 60)} minutes. The organiser may be offline; the last published information is still shown above.")
    if dt:
        st.caption(f"Last published: {dt.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')} · This page refreshes automatically.")
    else:
        st.caption("This page refreshes automatically.")


@st.fragment(run_every="5s")
def live_board():
    robot_param = st.query_params.get("robot")
    if robot_param:
        try:
            render_profile(int(robot_param))
        except (TypeError, ValueError):
            st.error("That robot profile link is invalid.")
        return
    row = fetch_current()
    if not row:
        st.info("There is no active published competition right now. Try again once the organiser enables Online Builder View.")
        return
    render_snapshot(row.get("snapshot") or {}, str(row.get("updated_at") or ""))


live_board()
