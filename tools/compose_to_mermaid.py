import json
import re
import sys


def safe_id(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", name)
    if not cleaned:
        cleaned = "item"
    if cleaned[0].isdigit():
        cleaned = "_" + cleaned
    return cleaned


def add_line(lines, text):
    lines.append(text)


def to_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_env(env):
    items = []
    if isinstance(env, dict):
        for k, v in env.items():
            items.append(f"{k}={v}")
    elif isinstance(env, list):
        for entry in env:
            items.append(str(entry))
    return items


def normalize_ports(ports):
    out = []
    for p in to_list(ports):
        if isinstance(p, dict):
            host = p.get("published") or p.get("host") or ""
            target = p.get("target") or p.get("container") or ""
            proto = p.get("protocol") or ""
            if host and target:
                out.append(f"{host}:{target}/{proto}".rstrip("/"))
            else:
                out.append(str(p))
        else:
            out.append(str(p))
    return out


def normalize_networks(nets):
    if isinstance(nets, dict):
        return list(nets.keys())
    return to_list(nets)


def normalize_volumes(vols):
    out = []
    for v in to_list(vols):
        if isinstance(v, dict):
            source = v.get("source") or v.get("src") or ""
            target = v.get("target") or v.get("dst") or v.get("destination") or ""
            mode = v.get("mode") or ""
            if source or target:
                out.append((source, target, mode))
            else:
                out.append((str(v), "", ""))
        else:
            parts = str(v).split(":")
            if len(parts) == 1:
                out.append((parts[0], "", ""))
            elif len(parts) == 2:
                out.append((parts[0], parts[1], ""))
            else:
                out.append((parts[0], parts[1], parts[2]))
    return out


def main():
    data = json.load(sys.stdin)
    services = data.get("services", {}) or {}
    networks = data.get("networks", {}) or {}
    volumes = data.get("volumes", {}) or {}

    lines = []
    add_line(lines, "flowchart LR")
    add_line(lines, "classDef svc fill:#e3f2fd,stroke:#1e88e5,stroke-width:1px;")
    add_line(lines, "classDef net fill:#f1f8e9,stroke:#7cb342,stroke-width:1px,stroke-dasharray: 4 2;")
    add_line(lines, "classDef vol fill:#fff3e0,stroke:#fb8c00,stroke-width:1px;")

    vol_nodes = {}

    # Networks nodes
    for net_name in networks.keys():
        nid = safe_id(f"net_{net_name}")
        add_line(lines, f"  {nid}((\"{net_name}\")):::net")

    # Volume nodes (named volumes)
    for vol_name in volumes.keys():
        vid = safe_id(f"vol_{vol_name}")
        label = f"{vol_name}"
        add_line(lines, f"  {vid}[(\"{label}\")]:::vol")
        vol_nodes[vol_name] = vid

    # Service nodes
    for svc_name, svc in services.items():
        label_lines = [svc_name]
        image = svc.get("image")
        build = svc.get("build")
        if image:
            label_lines.append(f"image: {image}")
        if build:
            if isinstance(build, dict):
                ctx = build.get("context")
                if ctx:
                    label_lines.append(f"build: {ctx}")
            else:
                label_lines.append(f"build: {build}")

        ports = normalize_ports(svc.get("ports"))
        if ports:
            label_lines.append("ports: " + ", ".join(ports))

        env = normalize_env(svc.get("environment"))
        if env:
            label_lines.append("env: " + ", ".join(env))

        nets = normalize_networks(svc.get("networks"))
        if nets:
            label_lines.append("net: " + ", ".join(nets))

        vols = normalize_volumes(svc.get("volumes"))
        if vols:
            vol_text = []
            for source, target, mode in vols:
                s = source
                if target:
                    s = f"{source}:{target}"
                if mode:
                    s = f"{s}:{mode}"
                vol_text.append(s)
            label_lines.append("vol: " + ", ".join(vol_text))

        label = "<br/>".join(label_lines)
        sid = safe_id(f"svc_{svc_name}")
        add_line(lines, f"  {sid}[\"{label}\"]:::svc")

    # Edges: depends_on, networks, volumes
    for svc_name, svc in services.items():
        sid = safe_id(f"svc_{svc_name}")

        for dep in to_list(svc.get("depends_on")):
            dep_name = dep if isinstance(dep, str) else str(dep)
            did = safe_id(f"svc_{dep_name}")
            add_line(lines, f"  {sid} -- depends_on --> {did}")

        for net_name in normalize_networks(svc.get("networks")):
            nid = safe_id(f"net_{net_name}")
            add_line(lines, f"  {sid} --- {nid}")

        for source, target, mode in normalize_volumes(svc.get("volumes")):
            if not source:
                continue
            vid = vol_nodes.get(source)
            if not vid:
                vid = safe_id(f"vol_{source}")
                label = source
                add_line(lines, f"  {vid}[(\"{label}\")]:::vol")
                vol_nodes[source] = vid
            add_line(lines, f"  {sid} --- {vid}")

    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()