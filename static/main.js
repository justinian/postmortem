function update(key, word) {
	let url = "/poem/" + key;
	return fetch(url, {
		"method": "POST",
		"body": word,
	})
	.then( resp => resp.text() )
	.then( text => {
		console.log("new key", text);
		return text;
	});
}

export function update_all(starting_key, words) {
	var promise = Promise.resolve(starting_key);
	for (const word of words) {
		if (word.length < 1) continue;
		promise = promise.then( key => {
			return update(key, word);
		});
	}

	return promise.then( key => {
		return update(key, "\n");
	});
}
