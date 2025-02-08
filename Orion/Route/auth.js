const express = require("express");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const User = require("/models/user");

const router = express.Router();

// Cadastro
router.post("/register", async (req, res) => {
  const { name, email, password } = req.body;

  // Verifica se o usuário já existe
  const userExists = await User.findOne({ email });
  if (userExists) return res.status(400).json({ message: "Usuário já existe" });

  // Criptografa a senha
  const hashedPassword = await bcrypt.hash(password, 10);

  // Cria o usuário
  const user = new User({ name, email, password: hashedPassword });
  await user.save();

  res.status(201).json({ message: "Usuário cadastrado com sucesso" });
});

// Login
router.post("/login", async (req, res) => {
  const { email, password } = req.body;

  const user = await User.findOne({ email });
  if (!user) return res.status(400).json({ message: "Usuário não encontrado" });

  // Verifica a senha
  const isMatch = await bcrypt.compare(password, user.password);
  if (!isMatch) return res.status(400).json({ message: "Senha incorreta" });

  // Gera o token JWT
  const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: "1h" });

  res.json({ token, user: { id: user._id, name: user.name, email: user.email } });
});

module.exports = router;
