
var dias  = document.getElementsByClassName('diagram');
for(i=0; i<dias.length; i++) {
var diagram = Diagram.parse(dias[i].textContent);
dias[i].textContent = '';
diagram.drawSVG(dias[i], {theme: 'hand'});
}




themes = {
	'xyz' : {		
				'x': 0,
				'y': 0,
				'line-width': 0,
				'line-length': 0,
				'text-margin': 20,
				'font-size': 24,
				'font-color': 'black',
				'line-color': '#7d939e',
				'element-color': 'rgba(0,0,0,0)',
				'fill': 'white',
				'yes-text': 'yes',
				'no-text': 'no',
				'arrow-end': 'block',
				'scale': 0.8,
				// style symbol types
				'symbols': {
				  'start': {
				    'font-color': 'white',
				    'element-color': 'rgba(0,0,0,0)'
				  },
				  'end':{
				    'class': 'end-element'
				  }
				},
				// even flowstate support ;-)
				'flowstate' : {
				  'past' : { 'fill' : '#34495d', 'font-color': 'white' },
				  'current' : {'fill' : '#fcb738', 'font-color': 'white' ,  'font-weight' : 'bold'},
				  'future' : { 'fill' : '#03a9f4', 'font-color': 'white' },
				  'request' : { 'fill' : 'blue', 'font-color': 'white' },
				  'invalid': {'fill' : '#444444', 'font-color': 'white','element-color': 'rgba(0,0,0,0.5)'},
				  'approved' : { 'fill' : '#3ab881', 'font-color': 'white' , 'font-color':'white',  'yes-text' : 'APPROVED', 'no-text' : 'n/a' },
				  'rejected' : { 'fill' : '#db5960', 'font-color': 'white' ,  'yes-text' : 'n/a', 'no-text' : 'REJECTED' }
				}
			}
};





var flows  = document.getElementsByClassName('flowchart');
for(i=0; i<flows.length; i++) {
var chart = flowchart.parse(flows[i].textContent);
flows[i].textContent = '';
chart.drawSVG(flows[i], themes['xyz']);
}

