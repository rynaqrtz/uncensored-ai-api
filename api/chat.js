const { chat } = require('../unces');

module.exports = async (req, res) => {
  const { prompt, new: newChat, temp, max, json: jsonOutput } = req.query;
  if (!prompt) return res.status(400).json({ error: 'Parameter "prompt" diperlukan' });

  try {
    const result = await chat(prompt, {
      newChat: newChat === 'true',
      temperature: parseFloat(temp) || 1.2,
      maxTokens: parseInt(max) || 100000,
      stream: false,
    });
    res.status(200).json(result);
  } catch (e) {
    res.status(500).json({ success: false, error: e.message, creator: 'rynaqrtz' });
  }
};
