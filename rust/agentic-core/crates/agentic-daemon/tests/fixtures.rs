//! Source: agentic-native-stack.md
//! Context: QN.3 Temporary Workspace Fixture
//! Extraction ID: CODE-107
//! Knowledge Links: KI-168
//! Status: scaffolded

pub struct TempWorkspace {
    path: PathBuf,
}

impl TempWorkspace {
    pub async fn from_template(template: &Path) -> Result<Self, TestError> {
        let path = std::env::temp_dir().join(format!(
            "agentic-test-{}",
            uuid::Uuid::now_v7()
        ));

        copy_recursively(template, &path).await?;

        Ok(Self { path })
    }

    pub fn path(&self) -> &Path {
        &self.path
    }
}

impl Drop for TempWorkspace {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.path);
    }
}