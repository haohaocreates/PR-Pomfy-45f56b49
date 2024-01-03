import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
	name: "millyarde.customnodes.pomfy",
	async setup() {
		function messageHandler(event) {
			const id = event.detail.id;
			const message = event.detail.message;
			const node = app.graph._nodes_by_id[id];
			if (node && node.displayMessage) {
				node.displayMessage(id, message);
			} else {
				console.log(`node ${id} couldn't handle a message`);
			}
		}
		api.addEventListener("pomfy-message-handler", messageHandler);
	},
});
