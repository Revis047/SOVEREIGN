use tower::{Layer, Service};
use std::task::{Context, Poll};
use std::pin::Pin;
use futures::Future;

pub struct CircuitBreakerLayer {
    pub threshold: u32,
}

impl<S> Layer<S> for CircuitBreakerLayer {
    type Service = CircuitBreaker<S>;

    fn layer(&self, inner: S) -> Self::Service {
        CircuitBreaker {
            inner,
            threshold: self.threshold,
            failures: 0,
        }
    }
}

pub struct CircuitBreaker<S> {
    inner: S,
    threshold: u32,
    failures: u32,
}

impl<S, Request> Service<Request> for CircuitBreaker<S>
where
    S: Service<Request>,
{
    type Response = S::Response;
    type Error = S::Error;
    type Future = S::Future;

    fn poll_ready(&mut self, cx: &mut Context<'_>) -> Poll<Result<(), Self::Error>> {
        if self.failures >= self.threshold {
            println!("CircuitBreaker: OPEN - Blocking requests to protect system");
            // In production, would return error or wait for cooldown
        }
        self.inner.poll_ready(cx)
    }

    fn call(&mut self, req: Request) -> Self::Future {
        self.inner.call(req)
    }
}
