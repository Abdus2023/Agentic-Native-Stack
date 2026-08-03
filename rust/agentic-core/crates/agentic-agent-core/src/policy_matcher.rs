//! Source: agentic-native-stack.md
//! Context: IW.2 Rust Matcher Sketch
//! Extraction ID: CODE-087
//! Knowledge Links: KI-153
//! Status: scaffolded

pub struct CompiledPolicy {
    rules: Vec<CompiledRule>,
}

impl CompiledPolicy {
    pub fn evaluate(
        &self,
        action: &str,
        resource: &str,
        env: &PolicyEnv,
    ) -> PolicyEffect {
        for rule in &self.rules {
            if rule.matches(action, resource, env) {
                return rule.effect;
            }
        }
        PolicyEffect::Ask
    }
}

pub struct CompiledRule {
    priority: u32,
    effect: PolicyEffect,
    action_matcher: Matcher,
    resource_matcher: Matcher,
    conditions: Vec<Condition>,
}

impl CompiledRule {
    pub fn matches(
        &self,
        action: &str,
        resource: &str,
        env: &PolicyEnv,
    ) -> bool {
        self.action_matcher.matches(action)
            && self.resource_matcher.matches(resource)
            && self.conditions.iter().all(|c| c.matches(env))
    }
}

#[derive(Debug, Clone, Copy)]
pub enum PolicyEffect {
    Allow,
    Deny,
    Ask,
}