import { useEffect } from 'react';
import { useState } from 'react';
import './ShowComments.css';

function ShowComments() {
	const [comments, setComments] = useState([]);

	useEffect(() => {
		const fetchComments = async () => {
			try {
				const response = await fetch('http://localhost:5000/api/comments');
				const data = await response.json();
				setComments(data);
			} catch (error) {
				console.error('Error fetching comments:', error);
			}
		};

		fetchComments();

	}, []);


	return (
		<>
			<table className="comments-table">
				<thead>
					<tr>
						<th className="comments-header">Username</th>
						<th className="comments-header">Comment</th>
					</tr>
				</thead>
				<tbody>
					{comments.map((comment, index) => (
						<tr key={index} className="comments-row">
							<td className="comments-username">{comment.username}</td>
							<td className="comments-text">{comment.comment_text}</td>
						</tr>
					))}
				</tbody>
			</table>

			{/* <div>
				{comments.map((comment, index) => (
					<div key={index} >
						<p>{comment.comment_text}</p>
					</div>
				))}
			</div> */}

		</>
	);

}

export default ShowComments