<template>
	<div id="iframe-wrapper" height="100%" width="100%" style="display: flex; width: 100%; height: 100%;">
		<iframe
		v-if="loaded"
		:src="iframe.src"
		frameborder="0" style="flex-grow: 1; border: none; margin: 0; padding: 0;"></iframe>
	</div>
</template>

<script lang="ts">
import Vue from "vue";
import kaapanaApiService from "@/common/kaapanaApi.service";

export default Vue.extend({
	name: "Application",
	watch: {
		'$route' (to, from) {
			this.getApplication();
		}
	},
	data: () => ({
		application: {links: [] as string[], releaseName: ""},
      	loaded: false,
		iframe: {
			src: "",
			style: null as any,
			wrapperStyle: null as any
		}
	}),
  	mounted() {
		this.getApplication();
	},
	methods: {
		getApplication() {
			let params = {
				repo: "kaapana-public",
			};
			kaapanaApiService
				.helmApiGet("/extensions", params)
				.then((response: any) => {
					this.application = response.data.find((i: any) => {
						return i.releaseName === this.$route.params.releaseName && i.kind === "application" && this.checkDeploymentReady(i) === true && i.successful !== 'pending';
					});
					if (this.application !== undefined) {
						this.iframe.src = this.application.links[0];
						this.loaded = true;
						window.document.title = this.application.releaseName;
					}
				})
				.catch((err: any) => {
					console.log(err);
				});
		},
    checkDeploymentReady(item: any) {
      if (item["multiinstallable"] == "yes" && item["chart_name"] == item["releaseName"]) {
        return false
      }
      if (item["available_versions"][item.version]["deployments"].length > 0) {
        return item["available_versions"][item.version]["deployments"][0].ready
      }
      return false
    },
	}
});
</script>