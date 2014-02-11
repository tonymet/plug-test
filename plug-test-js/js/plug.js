/**
 * global max const
 */
var MAX = 1E6;
/**
 * Converts a value to readable. 
 * @constructor
 * @param {int} value
 */
function ReadableNumber(value){
	this.value = value;
	this.stack = [];

	// consts for 1s, tens , etc
	this.ENGLISH = {
		1: ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'],
		1E1: ['', '', 'twenty', 'thirty', 'fourty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'],
		1E2: ['hundred'],
		1E3: ['thousand'],
		1E6: ['million']
	   
	};
	// pursuit order
	this.order = [1E6, 1E3, 1E2, 1E1, 1E0];
};

/**
 * @private
 * recursive method to parse number. 
 * SIDE-EFFECT: updates this.stack with string elements
 * @param {int} value to parse
 * 
 */
ReadableNumber.prototype._parseNumber = function(n){
	while(n > 0){
		for(i = 0; i < this.order.length; ++i){
			//quotient
			q = n / this.order[i];
			// TODO: add case for ten-thousands etc
			if(q > 1){
				// get int of q
				q = Math.floor(i);
				this.stack.push(this.ENGLISH[1][q - 1]);
				this.stack.push(this.ENGLISH[this.order[i]]);
				// keep the remainder
				n = n % this.order[i];
				// recurse on the remainder
				this._parseNumber(n);
			}
			// skip to next ordinal
		}
	}
}

/**
 * convert current ReadableNumber to string
 * @return {string}
 */
ReadableNumber.prototype.toString = function(){
	this.stack = []
	this._parseNumber(this.value);
	return this.stack.join(" ");
}

/**
 * tests plug iteratively for spec #2
 * @constructor
 */
function TestPlug(max){
	// TODO: set to 1E6
	this.MAX = max;
}

/**
 * iterates to this.MAX and 
 */
TestPlug.prototype.timeTest = function(){
	var t0 = window.performance.now();
	for(i= 1; i <= this.MAX; ++i){
		var rn = new ReadableNumber(i);
		var s = ReadableNumber.toString();
	}
	var t1 = window.performance.now();
	return t1 - t0;
}

/**
 * Attach to element and loop from 0 .. max
 * @constructor
 * @param {Element} the element to update
 */
function UILoop(e){
	this.element = e;
	this.cur = 0;
}

/**
 * Iterate over the loop using doInterval to prevent
 * hanging the UI
 */
UILoop.prototype.doInterval = function(){
	// save context for setInterval
	var _this = this;
	setInterval(function(){
		_this.cur +=1;
		rn = new ReadableNumber(this.cur);
		_this.element.val( "NUM: " + rn.toString());
		// interrupt at max and reverse
		if(_this.cur >= MAX ){
			clearInterval(this);
		}
		// TODO: reverse loop
	},10);
};

/**
 * wire-up the UI for the app
 *
 */
$(document).ready(function(){
	// wire u the loop widget click and assign the loop
	$('#input_widget button').click(function(){
		var rn = new ReadableNumber($('#input_widget .in input').val());
		$('#input_widget .out input').val(rn.toString());
	});
	$('#loop_widget button').click(function(){
		var u = new UILoop($('#loop_widget input'));
		u.doInterval();
	});

	$('#timer_widget  button').click(function(){
		var t = new TestPlug(MAX);
		button = this;
		// disable button while processing
		this.disabled = true;
		// call via setTimeout to prevent freezing UI
		setTimeout(function(){
			button.disabled = false;
			$('#timer_widget input').val('TIME: ' + t.timeTest());
		});
	});
	// wire up the slider
	$( "#slider" ).slider(
		{
			'max': MAX  
		}
	);
	$("#slider").on("slidechange",function(event, ui){
		rn = new ReadableNumber(this.cur);
		//$("slider_widget input").val( "SLIDER: " + rn.toString());
		$("#slider_widget input").val( "TEXT: " + rn.toString(ui.value));
	});
});
