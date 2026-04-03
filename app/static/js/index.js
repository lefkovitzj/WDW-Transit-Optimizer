document.addEventListener("DOMContentLoaded", () => {
    const FORM_KEY = "wdw_route_form_v1";
    const form = document.getElementById("routeForm");
    if (!form) return;

    const saveToStorage = () => {
      /* Save the current form state to local storage, including dynamic stops. */
      const data = {
        start: document.getElementById('start-dest-input')?.value || "",
        startDisplay: document.getElementById('start-display')?.value || "",
        end: document.getElementById('final-dest-input')?.value || "",
        endDisplay: document.getElementById('final-display')?.value || "",
        stops: []
      };

      // Grab all "Must-Visit Stops" - both hidden IDs and display labels.
      const stopWrappers = document.querySelectorAll('#stops-container [data-search-wrapper]');
      stopWrappers.forEach(wrapper => {
        const hiddenInput = wrapper.querySelector('input[type="hidden"]');
        const displayInput = wrapper.querySelector('input[type="text"]');
        
        if (displayInput && displayInput.value.trim() !== "") {
          data.stops.push({
            id: hiddenInput ? hiddenInput.value : "",
            label: displayInput.value
          });
        }
      });

      localStorage.setItem(FORM_KEY, JSON.stringify(data));
    };

    const restoreFromStorage = () => {
      /* Restore the form state from local storage, including dynamic stops. */
      try {
        const raw = localStorage.getItem(FORM_KEY);
        if (!raw) return;
        
        const saved = JSON.parse(raw);
        let hasData = false;

        // Restore "Starting Point".
        if (saved.startDisplay) {
          document.getElementById('start-display').value = saved.startDisplay;
          document.getElementById('start-dest-input').value = saved.start || "";

          hasData = true;
        }

        // Restore "Final Destination".
        if (saved.endDisplay) {
          document.getElementById('final-display').value = saved.endDisplay;
          document.getElementById('final-dest-input').value = saved.end || "";
          hasData = true;
        }

        // Restore Dynamic "Must-Visit Stops".
        if (Array.isArray(saved.stops) && typeof addStopField === 'function') {
          saved.stops.forEach(stop => {
            // Call the global function to add a new stop field.  
            addStopField(); 
            const currentStopId = `stop-${stopCount}`;
            const dInput = document.getElementById(`display-${currentStopId}`);
            const hInput = document.getElementById(`input-${currentStopId}`);
            
            if (dInput) dInput.value = stop.label;
            if (hInput) hInput.value = stop.id;
            hasData = true;
          });
        }
        return hasData;
      } catch (err) {
          console.error("WDW Wayfinder: Failed to restore route from local storage.", err);
          return false;
      }
    };

    // Add logic for the "Clear All" button to reset the form and clear storage.
    clearBtn = document.getElementById("clear-form-btn");
    if (clearBtn) {
        clearBtn.addEventListener("click", (e) => {
            e.preventDefault(); // Stop page reload
            
            // 1. Wipe Storage
            localStorage.removeItem(FORM_KEY);
            
            // 2. Reset standard fields
            form.reset();
            document.getElementById('start-dest-input').value = "";
            document.getElementById('final-dest-input').value = "";
            
            // 3. Remove dynamic stop rows (keeping the label)
            const stopContainer = document.getElementById('stops-container');
            if (stopContainer) {
                stopContainer.innerHTML = '<label class="block text-xs font-semibold uppercase tracking-wide text-slate-400">Must-Visit Stops</label>';
            }

            // 4. Clear the UI result area
            const results = document.getElementById('itinerary-result');
            if (results) {
                results.innerHTML = `
                    <div class="print:hidden rounded-xl border border-slate-800 bg-slate-900 p-6 shadow-soft">
                        <div class="flex items-start gap-3">
                            <div class="mt-0.5 h-5 w-5 rounded-full bg-wdw-navy2 text-center text-xs font-bold leading-5 text-white">i</div>
                            <div>
                                <h3 class="font-semibold text-slate-100">Ready to explore?</h3>
                                <p class="mt-1 text-sm text-slate-300">Select your starting location, optional intermediate stops, and final destination. WDW Wayfinder will generate the most efficient route.</p>
                            </div>
                        </div>
                    </div>`;
            }
        });
    }

    // Restore immediately on load.
    if (restoreFromStorage()) {
      // If there was data to restore, we trigger a route calculation.
      setTimeout(() => {
        htmx.trigger(form, "submit");
      }, 100);
    }

    // Save when the form is submitted via HTMX.
    form.addEventListener("htmx:configRequest", () => {
        saveToStorage();
    });
});