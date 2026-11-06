# Design inheritance and real interaction

Before changing UI appearance, find and actually inspect at least one reliable
visual reference: a screenshot of the existing interface, a Qt original design
or rendered .ui form, or a UI design/mockup. Capture the current app yourself
when it supplies the reference; a file name or unrendered markup alone is not
visual inspection. Identify which layout, style and interaction properties to
preserve. If no reference can be obtained and the visual direction is unresolved,
ask the user before choosing it. Continue independent work while waiting.

Also find the project's component library, design tokens, neighboring screens
and interaction conventions. A reference need not prescribe every pixel.

Prefer existing controls and patterns. Record a justified exception when adding
a new pattern. If existing design is part of the problem, propose a coherent
change across the affected surfaces instead of preserving a defect by habit.
Check component documentation and installed versions before copying API usage.

For material UI work answer the relevant questions:
- Which existing component, layout and token supplies each major element?
- What is the primary action and can the intended user find it?
- What does loading, empty, error, disabled and success look like?
- How do cancel, retry, back and re-entry behave?
- What changes on narrow screens, keyboard navigation and reduced motion?

A screenshot plus layout and state notes is often more useful than a screenshot
alone. For a new visual direction implement one representative page or
interaction first, inspect it, then extend it. Avoid inventing a separate design
system for each feature. Keep explanatory copy useful to the product's users.

Verify in the actual app and target viewport. For a CDP-capable host such as an
Electron or Chromium app, connect through an available CDP tool and confirm the
host process, target window/page and loaded build before capturing evidence.
A separate browser page or mockup does not establish host-app acceptance.
For native Qt or another target without CDP, use an appropriate desktop or UI
automation tool. Verify actual tool availability; do not assume a connection
because a descriptor or debugging port exists. If access is unavailable, state
which visual or interaction criteria remain unverified.

Capture and inspect relevant before/after states against the visual reference.
Perform representative clicks or equivalent user input, then check the resulting
state, navigation and persisted result where applicable. Calling a handler or
seeing a button alone does not prove the user path. A screenshot proves appearance,
not interaction. Inspect DOM, computed styles and box metrics when a layout fix
fails, rather than guessing another CSS patch.

Inspect the captured result itself. A capture named "populated" may still show
initial loading or an empty state; confirm that the intended content has arrived
and the relevant control is visible. An overlay fitting the viewport does not
establish that its items inherit the existing component style or remain readable
in the relevant interaction states. Review one representative result before
extending the same pattern across more surfaces.

Review against coherent design, craft and usability criteria calibrated with
project examples and user feedback. "Could it be prettier?" produces endless
opinions. Report a concrete mismatch and impact. Preserve a better intermediate
version when further changes worsen the result; a higher self-score is not proof.
