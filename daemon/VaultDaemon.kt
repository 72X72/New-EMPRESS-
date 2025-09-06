import java.io.File
import javax.crypto.Cipher
import javax.crypto.spec.SecretKeySpec

object VaultDaemon {
    private val key = "EMPRESSKEY123456".toByteArray() // 16-byte AES key

    fun sealLog(entry: String) {
        val encrypted = encrypt(entry)
        File("/empress/vault/mutation.log.enc").appendText("$encrypted\n")
    }

    private fun encrypt(data: String): String {
        val cipher = Cipher.getInstance("AES")
        val secretKey = SecretKeySpec(key, "AES")
        cipher.init(Cipher.ENCRYPT_MODE, secretKey)
        return cipher.doFinal(data.toByteArray()).joinToString("") { "%02x".format(it) }
    }
}
