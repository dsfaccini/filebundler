<tests>
    <test name="Project Loading Test">
        <description>Verify that projects load correctly, including file tree structure generation with proper ignore patterns applied. Test with both small and large projects to ensure performance.</description>
        <modules-involved>
            <module path="filebundler/ui/sidebar/project_selection.py">triggers the project loading</module>
            <module path="filebundler/FileBundlerApp.py">loads directory structure recursively</module>
            <module path="filebundler/managers/ProjectSettingsManager.py">loads project settings</module>
        </modules-involved>
    </test>

    <test name="File Selection Persistence Test">
        <description>Verify selections are properly persisted to disk when files are selected/unselected and correctly restored when reopening a project.</description>
        <modules-involved>
            <module path="filebundler/ui/sidebar/file_tree.py">handles file selection interactions</module>
            <module path="filebundler/managers/SelectionsManager.py">persists selections to disk</module>
        </modules-involved>
    </test>

    <test name="Bundle Creation and Management Test">
        <description>Test creating bundles with various file sets, verifying metadata is accurate (file count, size, word count) and bundle data is persisted correctly.</description>
        <modules-involved>
            <module path="filebundler/ui/tabs/selected_files.py">triggers bundle creation</module>
            <module path="filebundler/managers/BundleManager.py">persists bundles to disk</module>
            <module path="filebundler/models/Bundle.py">calculates bundle metadata</module>
        </modules-involved>
    </test>

    <test name="Bundle Activation Test">
        <description>Verify that activating a bundle correctly restores file selections and handles missing files gracefully.</description>
        <modules-involved>
            <module path="filebundler/ui/tabs/manage_bundles.py">triggers bundle activation</module>
            <module path="filebundler/managers/BundleManager.py">activates the bundle</module>
            <module path="filebundler/managers/SelectionsManager.py">updates selections based on bundle</module>
        </modules-involved>
    </test>

    <test name="Stale Detection Test">
        <description>Verify bundles are correctly marked as stale when files are modified after export, and that the UI indicates this status.</description>
        <modules-involved>
            <module path="filebundler/models/Bundle.py">detects stale status</module>
            <module path="filebundler/ui/tabs/manage_bundles.py">displays stale status</module>
        </modules-involved>
    </test>

    <test name="Export System Test">
        <description>Test exporting bundles to clipboard with various file types and contents, ensuring the XML formatting is correct and export statistics are updated.</description>
        <modules-involved>
            <module path="filebundler/ui/tabs/export_contents.py">triggers the export</module>
            <module path="filebundler/services/code_export_service.py">formats and exports content</module>
            <module path="filebundler/models/BundleMetadata.py">updates export statistics</module>
        </modules-involved>
    </test>

    <test name="Search Functionality Test">
        <description>Verify file tree search correctly filters files and directories, showing only matching items while maintaining proper tree structure.</description>
        <modules-involved>
            <module path="filebundler/ui/sidebar/file_tree.py">implements search filtering</module>
        </modules-involved>
    </test>

    <test name="Project Settings Test">
        <description>Test saving and loading project settings, particularly ignore patterns, and verify these settings are correctly applied when loading project files.</description>
        <modules-involved>
            <module path="filebundler/ui/sidebar/settings_panel.py">triggers settings updates</module>
            <module path="filebundler/managers/ProjectSettingsManager.py">persists project settings</module>
            <module path="filebundler/FileBundlerApp.py">applies settings during file loading</module>
        </modules-involved>
    </test>

    <test name="Global Settings Test">
        <description>Verify global settings are correctly saved and applied to new projects, particularly default ignore patterns.</description>
        <modules-involved>
            <module path="filebundler/ui/tabs/global_settings_panel.py">triggers global settings updates</module>
            <module path="filebundler/managers/GlobalSettingsManager.py">persists global settings</module>
        </modules-involved>
    </test>

    <test name="Project Refresh Test">
        <description>Verify project refresh correctly updates the file tree when files are added, modified, or deleted externally without losing current selections.</description>
        <modules-involved>
            <module path="filebundler/ui/sidebar/file_tree_buttons.py">triggers project refresh</module>
            <module path="filebundler/FileBundlerApp.py">refreshes file structure</module>
            <module path="filebundler/managers/SelectionsManager.py">maintains selections during refresh</module>
        </modules-involved>
    </test>

    <test name="Error Handling Test">
        <description>Test error handling for various failure scenarios: inaccessible files, malformed settings files, and permission issues. Verify appropriate error messages are shown.</description>
        <modules-involved>
            <module path="filebundler/ui/notification.py">displays error notifications</module>
            <module path="filebundler/FileBundlerApp.py">handles file system errors</module>
            <module path="filebundler/utils.py">handles serialization/deserialization errors</module>
        </modules-involved>
    </test>

    <test name="Large File Handling Test">
        <description>Test performance and memory usage when handling very large files or projects with many files, ensuring the application remains responsive.</description>
        <modules-involved>
            <module path="filebundler/FileBundlerApp.py">loads large file structures</module>
            <module path="filebundler/services/code_export_service.py">processes large exports</module>
        </modules-involved>
    </test>

    <test name="Recent Projects Test">
        <description>Verify the recent projects list is correctly updated when projects are opened and that selecting from this list correctly loads the project.</description>
        <modules-involved>
            <module path="filebundler/ui/sidebar/project_selection.py">displays and handles recent projects</module>
            <module path="filebundler/managers/GlobalSettingsManager.py">maintains recent projects list</module>
        </modules-involved>
    </test>

    <test name="UI Session State Test">
        <description>Test that all UI components properly handle Streamlit session state, maintaining proper state across reruns and page refreshes.</description>
        <modules-involved>
            <module path="filebundler/state.py">initializes session state</module>
            <module path="main.py">coordinates overall UI state</module>
        </modules-involved>
    </test>
</tests>