# What happens when we open a project?
main.py renders the UI element from project_selection.py on the sidebar. once we open a project, project_selection.py instantiates the app, assigns it to st.session_state.app, and calls app.load_project(), followed by an st.rerun().

the only time when the SelectionsManager and the BundleManager are instantiated is when we call app.load_project(). that's also the only time that their methods, load_selections() and load_bundles() are called. which is why we DON'T call st.rerun() in either of them.

