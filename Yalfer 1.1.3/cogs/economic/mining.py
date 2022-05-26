class MiningCogFunctionality:

	@staticmethod
	def delete_videocards(videocard, amount, guild, member, cursor, connection):
		cursor.execute(
			"SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ? AND graphics_cards_name = ?",
			(
				guild.id,
				member.id,
				videocard
			)
		)
		result = cursor.fetchone()
		if result[3] < amount:
			amount = result[3]
		cursor.execute(
			"UPDATE graphics_cards SET graphics_cards_amount = ? WHERE guild_id = ? AND member_id = ? AND "
			"graphics_cards_name = ?",
			(
				result[3] - amount,
				guild.id,
				member.id,
				videocard
			)
		)
		connection.commit()

	@staticmethod
	def add_videocard(videocard, amount, guild, member, cursor, connection):
		cursor.execute(
			"SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ? AND graphics_cards_name = ?",
			(
				guild.id,
				member.id,
				videocard
			)
		)
		result = cursor.fetchone()
		if result is None:
			cursor.execute(
				"INSERT INTO graphics_cards VALUES (?, ?, ?, ?)",
				(
					guild.id,
					member.id,
					videocard,
					amount
				)
			)
		else:
			cursor.execute(
				"UPDATE graphics_cards SET graphics_cards_amount = ? WHERE guild_id = ? AND member_id = ? AND "
				"graphics_cards_name = ?",
				(
					result[3] + amount,
					guild.id,
					member.id,
					videocard
				)
			)
		connection.commit()
		return


	@staticmethod
	def DB_mining_set(cursor, connection, ctx, value: bool):
		cursor.execute(
			"DELETE FROM  is_mining WHERE guild_id = ? AND member_id = ?",
			(
				ctx.guild.id,
				ctx.message.author.id
			)
		)
		cursor.execute("INSERT INTO is_mining VALUES (?, ?, ?)",
					   (
						   ctx.guild.id,
						   ctx.message.author.id,
						   int(value)
					   )
					   )
		connection.commit()
