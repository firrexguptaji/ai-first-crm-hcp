import LeftPanel from "./LeftPanel";
import RightPanel from "./RightPanel";

import "./layout.css";

export default function SplitLayout() {
    return (
        <main className="split-layout">
            <LeftPanel />
            <RightPanel />
        </main>
    );
}