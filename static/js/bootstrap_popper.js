//BootstrapのPopperを使用するためのJS
(function() {
	window.addEventListener("load", function () {
		$('[data-toggle="popover"]').popover();
	});
})();