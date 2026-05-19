// Wait for the DOM to load fully
document.addEventListener("DOMContentLoaded", function () {
    // Check if we have the content or description textareas on the page
    const contentTextarea = document.getElementById("id_content");
    const descTextarea = document.getElementById("id_description");

    if (contentTextarea || descTextarea) {
        console.log("Found editor fields, loading CKEditor...");
        
        // Dynamically load CKEditor script from CDN
        const script = document.createElement("script");
        script.src = "https://cdn.ckeditor.com/4.16.2/standard/ckeditor.js";
        script.onload = function () {
            console.log("CKEditor script loaded successfully.");
            
            // Once CKEditor is loaded, initialize it on the textareas
            if (contentTextarea) {
                CKEDITOR.replace("id_content", {
                    height: 450,
                    removePlugins: "about",
                    // Configure toolbar for text styling, links, lists, and tables
                    toolbarGroups: [
                        { name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
                        { name: 'editing', groups: [ 'find', 'selection', 'spellchecker' ] },
                        { name: 'links', groups: [ 'links' ] },
                        { name: 'insert', groups: [ 'insert' ] },
                        { name: 'forms', groups: [ 'forms' ] },
                        { name: 'tools', groups: [ 'tools' ] },
                        { name: 'document', groups: [ 'mode', 'document', 'doctools' ] },
                        { name: 'others', groups: [ 'others' ] },
                        '/',
                        { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
                        { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
                        { name: 'styles', groups: [ 'styles' ] },
                        { name: 'colors', groups: [ 'colors' ] }
                    ]
                });
            }
            if (descTextarea) {
                CKEDITOR.replace("id_description", {
                    height: 350,
                    removePlugins: "about"
                });
            }
        };
        document.head.appendChild(script);
    }
});
