// author: snicolet
// creation date: 19/10/2017
// version: 1.2

class AjaxForm {
	constructor(formObject, pbar=false) {
		this.formObject = formObject
		this.httpUrl = formObject.attributes.action.value;
		this.httpMethod = formObject.attributes.method.value;
		this.lock = false;
		this.pbar = pbar;
	};

	send() {
		if (this.lock)
			return (false);
		if (!this.formObject.checkValidity()) {
			this.invalid();
			return (false);
		}
		this.formObject.disabled = true;
		this.lock = true;
		var data = new FormData(this.formObject)
		var req = new XMLHttpRequest();
		// les methodes XMLHttpRequest ecrasent "this" donc je le stoque dans un self
		var self = this;
		var func_end = function(evt) {
			console.log('all done');
			self.lock = false;
			self.formObject.disabled = false;
			self.finish();
		};
		var func_error = function (evt) { self.error(self, evt); };

		// si une progress bar est la on met la valeur a 100%
		var func_success = function(evt) {
			if (self.pbar)
				self.pbar.setValue(100);
			self.success(self, evt);
		};

		// fonction de gestion de la progression, elle calcule un coeficiant
		// qui va de 0.0 a 1.0 (float)
		var func_progress = function(evt) {
			var percent;
			if (evt.lengthComputable)
				percent = evt.loaded / evt.total;
			else
				percent = 0.0;
			if (self.pbar)
				self.pbar.setValue(Math.round(percent * 100.0));
			self.progress(self, evt, percent);
		};
		req.addEventListener("load", func_success, false);
		req.addEventListener("error", func_error, false);
		req.upload.addEventListener("progress", func_progress, false);
		req.addEventListener("loadend", func_end, false);
		if (this.pbar)
			this.pbar.setValue(0);
		if (this.setup(req) == false) {
			this.lock = false;
			self.formObject.disabled = false;
			self.finish();
			return (false);
		}
		req.open(this.httpMethod, this.httpUrl, true);
		console.log('starting upload...');
		req.send(data);
		console.log('request sent');
		return (false);
	};

	success(self, evt) {
		console.log("success, received", evt);
	};

	error(self, evt) {
		console.log("error, received", evt);
	};

	invalid(self) {
		console.log("the form is invalid or a field is missing");
	};

	progress(self, evt, pc) {
		console.log("progress state:", pc);
	};

	finish(self) {
		// will be called after any transactin, even in case of an error
	};

	setup(req) {
		// overload this method to configure custom headers in the request
		// it's also here to setup any eventListener
		// req.setRequestHeader("X-Foo", "bar");
	};
}
