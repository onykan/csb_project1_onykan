// A script to display POSIX timestamps as localised time format
addEventListener("DOMContentLoaded", (event) => {
    const timestamps = document.querySelectorAll(".timestamp");
    const formator = new Intl.DateTimeFormat([window.navigator.language, "en-US"], {
        timeStyle: "short",
        dateStyle: "short"
    });

    timestamps.forEach((t) => {
        //console.log(t.textContent);
        try {
            t.textContent = formator.format(new Date(parseInt(t.textContent)));
        }
        catch (err) {
            console.error("Failed to parse and format timestamp for a post...");
            console.error(err);
        }
    });
});